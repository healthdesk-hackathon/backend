import os
import string

from common.base_models import ImmutableBaseModel, CurrentBaseModel
from patient.models import Patient
from equipment.models import Bed, BedType

from random import choice
from barcode import EAN13
from barcode.writer import ImageWriter
from django.conf import settings
from django.core.files.images import ImageFile
from django.db import transaction
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Count, F, Avg, Subquery, OuterRef, Max
from django.utils import timezone as tz


class BedAssignment(ImmutableBaseModel):
    admission = models.ForeignKey('Admission', related_name='assignments', on_delete=models.CASCADE)
    bed = models.ForeignKey('equipment.Bed', related_name='assignments', on_delete=models.CASCADE)
    assigned_at = models.DateTimeField(auto_now_add=True)
    unassigned_at = models.DateTimeField(null=True, blank=True, default=None)

    class BedAssignmentManager(models.Manager):

        def current_per_severity(self):
            qs = self.get_queryset()
            qs = qs.filter(unassigned_at__isnull=True)
            qs = qs.annotate(label=F('bed__bed_type__name'))
            qs = qs.order_by('label')
            qs = qs.values('label')
            qs = qs.annotate(value=Count('label'))
            return qs

    objects = BedAssignmentManager()

    @transaction.atomic
    def save(self, **kwargs):
        super().save(**kwargs)
        bed = self.bed
        if self.unassigned_at:
            bed.state = Bed.StateChoices.OUT_OF_SERVICE
            bed.reason = Bed.ReasonChoices.CLEANING
        else:
            bed.state = Bed.StateChoices.ASSIGNED
            bed.reason = None
        bed.save()

    def __str__(self):
        return str(self.bed.id)

    class Meta:
        ordering = ['-assigned_at']


class Admission(CurrentBaseModel):
    """
    Represents the admission into the hospital system, when the admins / triage have
    performed the initial steps for getting the patient into the system.

    This class not only represents the action of admission, but also the person as they move
    around inside the hospital system. This saves us having to reference up to the 'Patient'
    record, the parent of this.
    """

    class AdmissionManager(models.Manager):
        def accepted(self):
            return self.get_queryset().filter(admitted_at__isnull=False)

        def rejected(self):
            return self.get_queryset().filter(admitted_at__isnull=True)

        def average_duration(self):
            qs = self.get_queryset()
            qs = qs.annotate(nb_discharges=Count('discharge_events')).exclude(nb_discharges=0)
            qs = qs.annotate(left_at=Subquery(
                BedAssignment.objects.filter(unassigned_at__isnull=False)
                .filter(admission=OuterRef('pk'))
                .annotate(max=Max('unassigned_at'))
                .values('max'),
                num=models.DateTimeField()
            ))
            qs = qs.values('admitted_at', 'left_at')
            average_duration = qs.aggregate(average_duration=Avg(F('left_at') - F('admitted_at')))['average_duration']
            return average_duration

        def admissions_per_day(self):
            qs = self.accepted()
            qs = qs.order_by('admitted_at')
            qs = qs.extra(select={'day': 'date(admitted_at)'})
            all_results = [[x.day, x.health_snapshots.order_by(
                'created')[0].severity] for x in qs if x.health_snapshots.order_by('created').count() > 0]
            admissions = {}
            for [day, label] in all_results:
                if day not in admissions:
                    admissions[day] = {}
                if label not in admissions[day]:
                    admissions[day][label] = 0
                admissions[day][label] += 1
            return [{'date': key, 'count': [{'label': label, 'value': count} for [label, count] in value.items()]} for
                    [key, value] in admissions.items()]

    objects = AdmissionManager()

    local_barcode = models.CharField(max_length=13, unique=True, null=True)
    local_barcode_image = models.ImageField(null=True)

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='admissions', null=False)
    admitted_at = models.DateTimeField(null=True, default=None)
    admitted = models.BooleanField(default=True)

    @property
    def patient_display(self):
        if self.patient and self.patient.personal_data:
            data = self.patient.personal_data
            return f'{data.first_name} {data.last_name}'
        else:
            return '-'

    def generate_barcode_image(self):

        image = ImageFile(f'/tmp/{self.local_barcode}.jpeg')

        with open(image.file, 'wb') as f:
            EAN13(self.local_barcode, writer=ImageWriter()).write(f)

        with open(image.file, 'rb') as f:
            self.local_barcode_image.save(f'{self.local_barcode}.jpeg', ImageFile(f), save=False)

        os.unlink(image.file)

    def save(self, **kwargs):
        if not self.local_barcode:
            local_barcode = ''.join(choice(string.digits) for _ in range(13))
            while Admission.objects.filter(local_barcode=local_barcode).exists():
                local_barcode = ''.join(choice(string.digits) for _ in range(13))
            self.local_barcode = local_barcode

        if not self.admitted_at and self.admitted:
            self.admitted_at = tz.now()

        super().save(**kwargs)
        self.generate_barcode_image()

    @property
    def current_severity(self):
        snapshot = self.health_snapshots.first()
        return snapshot.severity if snapshot else None

    @property
    def current_bed(self):
        try:
            return self.assignments.filter(unassigned_at__isnull=True).latest('-assigned_at').bed
        except BedAssignment.DoesNotExist:
            return None

    @transaction.atomic
    def assign_bed(self, bed_type):
        current_bed = self.current_bed

        if current_bed:
            assignment = BedAssignment.objects.get(bed=current_bed, admission=self)
            assignment.unassigned_at = tz.now()
            assignment.save()

        new_bed = bed_type.beds.available().first()
        if not new_bed:
            raise Bed.DoesNotExist(f'There are no bed available for this type: {bed_type.name}')
        assignment = BedAssignment(admission=self, bed=new_bed, current_user=self.current_user)
        assignment.save()
        return new_bed

    def discharge(self):
        res = Discharge(admission=self, current_user=self.current_user)
        res.save()
        return res

    def record_deceased(self):
        res = Deceased(admission=self, current_user=self.current_user)
        res.save()
        return res

    @property
    def is_discharged(self):
        return self.discharge_events.first() is not None

    def discharged(self):
        return self.is_discharged

    discharged.boolean = True

    @property
    def is_deceased(self):
        return self.deceased_event is not None

    def deceased(self):
        return self.is_deceased
    deceased.boolean = True

    def __str__(self):
        return f'{str(self.id)[:12]}'


class HealthSnapshot(ImmutableBaseModel):
    class SeverityChoices(models.TextChoices):
        RED = 'RED', 'Red'
        YELLOW = 'YELLOW', 'Yellow'
        GREEN = 'GREEN', 'Green'
        WHITE = 'WHITE', 'White'

    admission = models.ForeignKey(Admission, on_delete=models.PROTECT, related_name='health_snapshots')

    blood_pressure_systolic = models.PositiveIntegerField(null=True, blank=True)
    blood_pressure_diastolic = models.PositiveIntegerField(null=True, blank=True)
    heart_rate = models.PositiveIntegerField(null=True, blank=True)
    breathing_rate = models.PositiveIntegerField(null=True, blank=True)
    temperature = models.FloatField(null=True, blank=True)
    oxygen_saturation = models.PositiveIntegerField(null=True, blank=True)

    gcs_eye = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(4)], null=True,
                                               blank=True, verbose_name='GCS eye')
    gcs_verbal = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], null=True,
                                                  blank=True, verbose_name='GCS verbal')
    gcs_motor = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(6)], null=True,
                                                 blank=True, verbose_name='GCS motor')

    observations = models.TextField(null=True, blank=True)

    severity = models.CharField(max_length=6, choices=SeverityChoices.choices)

    @property
    def gcs_total(self):
        if self.gcs_eye is None or self.gcs_verbal is None or self.gcs_motor is None:
            return 0
        return self.gcs_eye + self.gcs_verbal + self.gcs_motor

    def __str__(self):
        return f'{self.created} - {self.severity or ""}'

    class Meta:
        ordering = ['-created']


class Discharge(ImmutableBaseModel):
    """
    Represents the discharge from the hospital system, when the admins / triage have
    completed any steps to release them.
    """

    admission = models.ForeignKey(Admission, on_delete=models.CASCADE, null=False, related_name='discharge_events')
    discharged_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(null=True, blank=True)

    @transaction.atomic
    def save(self):
        """override save to handle the (re)assignment of a patient to a bed
        """
        # Complete the discharge save
        super().save()

        # Does the current admission have an assigned bed already?
        bed = self.admission.current_bed
        if bed:
            # Release the current bed and assign the new one
            bed.leave_bed()


class Deceased(ImmutableBaseModel):
    """
    The patient is deceased. Any additional workflow can continue from here.
    Additionally, the bed is released.
    """

    admission = models.OneToOneField(Admission, on_delete=models.CASCADE, null=False, related_name='deceased_event')
    registered_at = models.DateTimeField(null=True)

    cause = models.CharField(blank=False, null=False, max_length=100)
    notes = models.TextField(null=True, blank=True)
    notified_next_of_kin = models.BooleanField(default=False)


class HealthSnapshotFile(ImmutableBaseModel):
    image_path = 'health_snapshot_file'

    patient = models.ForeignKey(HealthSnapshot, on_delete=models.CASCADE, related_name='health_snapshot_files')
    file = models.ImageField(upload_to=image_path)
    notes = models.TextField()


class OverallWellbeing(ImmutableBaseModel):
    """
    Overall wellbeing, as the patient assesses themselves

    Attributes:
        overall_value: has a value 0 to 10 inclusive, representing how they feel
                        (0 awful, 10 amazing)

    Alternative is to reverse it:
    How bad did you, or do you, feel?
    Unnoticeable..Worst feeling ever


    """

    admission = models.OneToOneField(Admission, on_delete=models.CASCADE, related_name='overall_wellbeing')
    overall_value = models.IntegerField(null=False, validators=[MaxValueValidator(10), MinValueValidator(0)])


class CommonSymptoms(ImmutableBaseModel):
    """
    Symptoms that a patient believes they have.

    """

    admission = models.OneToOneField(Admission, on_delete=models.CASCADE, related_name='common_symptoms')

    chills = models.BooleanField(default=False, null=False)
    achy_joints_muscles = models.BooleanField(default=False, null=False)
    lost_taste_smell = models.BooleanField(default=False, null=False)
    congestion = models.BooleanField(default=False, null=False)
    stomach_disturbance = models.BooleanField(default=False, null=False)
    tiredness = models.BooleanField(default=False, null=False)
    headache = models.BooleanField(default=False, null=False)
    dry_cough = models.BooleanField(default=False, null=False)
    cough_with_sputum = models.BooleanField(default=False, null=False)
    nauseous = models.BooleanField(default=False, null=False)
    short_of_breath = models.BooleanField(default=False, null=False)
    sore_throat = models.BooleanField(default=False, null=False)
    fever = models.BooleanField(default=False, null=False)
    runny_nose = models.BooleanField(default=False, null=False)


class GradedSymptoms(ImmutableBaseModel):
    """
    Symptoms that a patient grades on a scale of 0 to 10
    """

    admission = models.OneToOneField(Admission, on_delete=models.CASCADE, related_name='graded_symptoms')

    # How hard is it to breath
    difficulty_breathing = models.IntegerField(null=False, validators=[MaxValueValidator(10), MinValueValidator(0)])
    # How anxious do you feel?
    anxious = models.IntegerField(null=False, validators=[MaxValueValidator(10), MinValueValidator(0)])


class RelatedConditions(ImmutableBaseModel):
    """
    How is your health?
    """

    admission = models.OneToOneField(Admission, on_delete=models.CASCADE, related_name='related_conditions')

    heart_condition = models.BooleanField(null=False, default=False)
    high_blood_pressure = models.BooleanField(null=False, default=False)
    asthma = models.BooleanField(null=False, default=False)
    chronic_lung_problems = models.BooleanField(null=False, default=False)
    mild_diabetes = models.BooleanField(null=False, default=False)
    chronic_diabetes = models.BooleanField(null=False, default=False)
    current_chemo = models.BooleanField(null=False, default=False)
    past_chemo = models.BooleanField(null=False, default=False)
    take_immunosuppressants = models.BooleanField(null=False, default=False)
    pregnant = models.BooleanField(null=False, default=False)
    smoke = models.BooleanField(null=False, default=False)






