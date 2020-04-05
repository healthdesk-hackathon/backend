import os
import string
import uuid
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


def prevent_update(pk):
    """prevent a record from being saved if it has a pk
    """

    if pk:
        raise ValidationError(
            'record must not be updated'
        )


class Patient(models.Model):
    """
    Central crosswalk model to connect all related records for a unique patient
    """

    anon_patient_id = models.CharField(max_length=12, default=None, unique=True)

    def __str__(self):
        return self.anon_patient_id

    @property
    def current_admission(self):
        return self.admissions.latest('-admitted_at')


class BedAssignment(models.Model):
    admission = models.ForeignKey('Admission', related_name='assignments', on_delete=models.CASCADE)
    bed = models.ForeignKey('Bed', related_name='assignments', on_delete=models.CASCADE)
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


class Admission(models.Model):
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
            all_results = [[x.day, x.health_snapshots.order_by('created_at')[0].severity] for x in qs]
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

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    local_barcode = models.CharField(max_length=13, unique=True, null=True)
    local_barcode_image = models.ImageField(null=True)

    # TODO: remove null=True below or fix the __str__ method
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='admissions', null=True)
    admitted_at = models.DateTimeField(null=True, default=None)
    admitted = models.BooleanField(default=True)

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
        assignment = BedAssignment(admission=self, bed=new_bed)
        assignment.save()
        return new_bed

    def discharge(self):
        res = Discharge(admission=self)
        res.save()
        return res

    def record_deceased(self):
        res = Deceased(admission=self)
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

        return f'{self.patient.anon_patient_id or ""} - {str(self.id)[:12]}'


class HealthSnapshot(models.Model):
    class SeverityChoices(models.TextChoices):
        RED = 'RED', 'Red'
        YELLOW = 'YELLOW', 'Yellow'
        GREEN = 'GREEN', 'Green'
        WHITE = 'WHITE', 'White'

    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='health_snapshots', on_delete=models.SET_NULL,
                             null=True)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    admission = models.ForeignKey(Admission, on_delete=models.PROTECT, related_name='health_snapshots')
    created_at = models.DateTimeField(auto_now_add=True)

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
        return f'{self.created_at} - {self.severity or ""}'

    class Meta:
        ordering = ['-created_at']


class Discharge(models.Model):
    """
    Represents the discharge from the hospital system, when the admins / triage have
    completed any steps to release them.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
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


class Deceased(models.Model):
    """
    The patient is deceased. Any additional workflow can continue from here.
    Additionally, the bed is released.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    admission = models.OneToOneField(Admission, on_delete=models.CASCADE, null=False, related_name='deceased_event')
    registered_at = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    cause = models.CharField(blank=False, null=False, max_length=100)
    notes = models.TextField(null=True, blank=True)
    notified_next_of_kin = models.BooleanField(default=False)

    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='recorded_deceased', on_delete=models.SET_NULL,
                             null=True)


class Bed(models.Model):
    """
    Individual bed resources that can be assigned to a patient.
    """

    class ReasonChoices(models.TextChoices):
        CLEANING = 'cleaning', 'Cleaning'
        EQUIP_FAIL = 'equip fail', 'Equipment failure'
        UNAVAILABLE = 'unavailable', 'Unavailable'

    class StateChoices(models.IntegerChoices):
        OUT_OF_SERVICE = 0, 'Out of service'
        ASSIGNED = 1, 'Assigned'
        AVAILABLE = 2, 'Available'

    class BedManager(models.Manager):

        def assigned(self):
            return self.get_queryset().filter(state=Bed.StateChoices.ASSIGNED)

        def available(self):
            return self.get_queryset().filter(state=Bed.StateChoices.AVAILABLE)

        def out_of_service(self):
            return self.get_queryset().filter(state=Bed.StateChoices.OUT_OF_SERVICE)

    objects = BedManager()

    def delete(self, using=None, keep_parents=False):
        if self.state == self.StateChoices.AVAILABLE:
            raise ValidationError('You cannot delete a bed that is in use')
        self.state = self.StateChoices.OUT_OF_SERVICE
        self.reason = self.ReasonChoices.UNAVAILABLE
        self.save()

    bed_type = models.ForeignKey('BedType', on_delete=models.CASCADE, null=False, related_name='beds')

    admissions = models.ManyToManyField(Admission, through=BedAssignment, related_name='assigned_beds')

    reason = models.CharField(max_length=20, choices=ReasonChoices.choices, null=True, blank=True)
    state = models.PositiveSmallIntegerField(choices=StateChoices.choices, default=StateChoices.AVAILABLE)

    @property
    def current_admission(self):
        assignment = self.assignments.filter(unassigned_at__isnull=True).first()
        if assignment:
            return assignment.admission
        return None

    def clean(self):
        if self.reason == self.StateChoices.OUT_OF_SERVICE and not self.state:
            raise ValidationError('Please provide the reason for this bed to be out of service')

    def save(self, **kwargs):
        self.clean()
        if self.state != self.StateChoices.OUT_OF_SERVICE:
            self.reason = None
        super().save(**kwargs)

    @transaction.atomic
    def leave_bed(self):
        """The patient is leaving the bed. The current assignment to this patient can be removed.

        The bed must be taken out of service for cleaning.
        """
        admission = self.current_admission

        assignment = self.assignments.filter(admission=admission, unassigned_at__isnull=True).first()
        if assignment:
            assignment.unassigned_at = tz.now()
            assignment.save()

    def __str__(self):
        return self.bed_type.name


class BedType(models.Model):
    """The numbers of each type of bed that a hospital has as resources.

    We want a manager to be able to view the number of beds of each type / number occupied /
    number out of service (cleaning)

    """

    class SeverityMatchChoices(models.TextChoices):
        RED = 'RED', 'Red'
        YELLOW = 'YELLOW', 'Yellow'
        GREEN = 'GREEN', 'Green'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50, blank=False)
    severity_match = models.CharField(max_length=6, blank=True, choices=SeverityMatchChoices.choices)
    total = models.IntegerField(null=False)

    def save(self, **kwargs):
        super().save(**kwargs)
        nb_to_create = self.total - self.beds.count()
        if nb_to_create <= 0:
            return
        for i in range(nb_to_create):
            b = Bed(bed_type=self)
            b.save()

    @property
    def number_out_of_service(self):
        return self.beds.out_of_service().count()

    @property
    def number_assigned(self):
        return self.beds.assigned().count()

    @property
    def number_available(self):
        return self.beds.available().count()

    @property
    def number_waiting(self):
        return self.waiting_for_assigned_beds.count()

    @property
    def is_available(self):
        """Check if this bed type is available for a new patient
        """
        return self.number_available > 0

    def __str__(self):
        return self.name

    @staticmethod
    def match_severity(severity):
        bed_types = BedType.objects.filter(severity_match=severity)
        if len(bed_types) == 0:
            return None
        else:
            return bed_types[0]


class HealthSnapshotFile(models.Model):
    image_path = 'health_snapshot_file'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    submission = models.ForeignKey(HealthSnapshot, on_delete=models.CASCADE, related_name='health_snapshot_files')
    file = models.ImageField(upload_to=image_path)
    notes = models.TextField()
