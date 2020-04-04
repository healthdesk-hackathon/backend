import hashlib
import uuid

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from patient_tracker.models import Patient, Admission, HealthSnapshot


class Submission(models.Model):
    """
    Submission record, ties all submission related info together.
    A submission may be a single patient, but we may have multiple submissions for a single patient too
    Once a hospital has verified the submission, we link back to the verified master record
    identifier: some kind of user entered id
    id_type:
    insurance number, phone number, email, etc
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    identifier = models.CharField(max_length=50, null=False)
    id_type = models.CharField(max_length=50, null=False)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, blank=True, null=True, related_name='submissions')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    @property
    def patient_anon_id(self):
        return hashlib.md5(self.id_type.encode() + self.identifier.encode()).hexdigest()[:12]

    def save(self, **kwargs):
        if not self.patient:
            patient_id = self.patient_anon_id
            patient, _ = Patient.objects.get_or_create(anon_patient_id=patient_id)
            self.patient = patient
        super().save(**kwargs)


class PersonalData(models.Model):
    class GenderChoices(models.TextChoices):
        MALE = 'M', 'Male'
        FEMALE = 'F', 'Female'
        OTHER = 'O', 'Other/Prefer not to disclose'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE, related_name='personal_data')
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    gender = models.CharField(max_length=1, choices=GenderChoices.choices)
    date_of_birth = models.DateField(auto_now=False, auto_now_add=False)


class Phone(models.Model):
    """
    Represents a phone number to be used identification or contact with the person
    phone type: mobile, home, work
    verified: has the phone actually be tried and the owner verified
    rank: is the order of preference for using a phone for contact
    0 - do not use
    > 0 - increasing preference
    disabled: do not use or show this record
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE, related_name='phones')
    phone_number = models.CharField(max_length=50)
    phone_type = models.CharField(max_length=10)
    rank = models.IntegerField()
    verified = models.BooleanField(default=False, null=False)
    disabled = models.BooleanField(default=False, null=False)


class OverallWellbeing(models.Model):
    """
    Overall wellbeing, as the patient assesses themselves

    Attributes:
        overall_value: has a value 0 to 10 inclusive, representing how they feel
                        (0 awful, 10 amazing)

    Alternative is to reverse it:
    How bad did you, or do you, feel?
    Unnoticeable..Worst feeling ever


    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    submission = models.OneToOneField(Submission, on_delete=models.CASCADE, related_name='overall_wellbeing')
    overall_value = models.IntegerField(null=False, validators=[MaxValueValidator(10), MinValueValidator(0)])


class CommonSymptoms(models.Model):
    """
    Symptoms that a patient believes they have.

    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    submission = models.OneToOneField(Submission, on_delete=models.CASCADE, related_name='common_symptoms')

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


class GradedSymptoms(models.Model):
    """
    Symptoms that a patient grades on a scale of 0 to 10
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    submission = models.OneToOneField(Submission, on_delete=models.CASCADE, related_name='graded_symptoms')

    # How hard is it to breath
    difficulty_breathing = models.IntegerField(null=False, validators=[MaxValueValidator(10), MinValueValidator(0)])
    # How anxious do you feel?
    anxious = models.IntegerField(null=False, validators=[MaxValueValidator(10), MinValueValidator(0)])


class RelatedConditions(models.Model):
    """
    How is your health?
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    submission = models.OneToOneField(Submission, on_delete=models.CASCADE, related_name='related_conditions')

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


class MedicalCenter(models.Model):
    """
    Available medical centers, from which a patient can choose.

    This is as limited set of attributes, to reflect what is needed for a simple,
    GPS located submission.

    Addtional address information could be added in the future if necessary.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    name = models.CharField(max_length=50, blank=False)
    latitude = models.FloatField(null=False)
    longitude = models.FloatField(null=False)


class ChosenMedicalCenter(models.Model):
    """
    The patient has selected a preferred medical center. Record this selection
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    submission = models.OneToOneField(Submission, on_delete=models.CASCADE, related_name='chosen_medical_center')

    medical_center = models.ForeignKey(MedicalCenter, on_delete=models.CASCADE, related_name='medical_center')


class InitialHealthSnapshot(models.Model):
    class SeverityChoices(models.TextChoices):
        RED = 'RED', 'Red'
        YELLOW = 'YELLOW', 'Yellow'
        GREEN = 'GREEN', 'Green'
        WHITE = 'WHITE', 'White'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    submission = models.OneToOneField(Submission, on_delete=models.CASCADE, related_name='initial_health_snapshot')
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

    def save(self, **kwargs):
        super().save(**kwargs)
        self.create_admission()

    def create_admission(self):
        """ Create an admission if the severity was not 'white', indicating dismiss without admission"""
        if self.severity == InitialHealthSnapshot.SeverityChoices.WHITE:
            return

        admission = Admission(patient=self.submission.patient)
        admission.save()

        health_snapshot = HealthSnapshot(admission=admission,
                                         blood_pressure_systolic=self.blood_pressure_systolic,
                                         blood_pressure_diastolic=self.blood_pressure_diastolic,
                                         heart_rate=self.heart_rate,
                                         breathing_rate=self.breathing_rate,
                                         temperature=self.temperature,
                                         oxygen_saturation=self.oxygen_saturation,
                                         gcs_eye=self.gcs_eye,
                                         gcs_verbal=self.gcs_verbal,
                                         gcs_motor=self.gcs_motor,
                                         observations=self.observations,
                                         severity=self.severity,
                                         #   user=self.user
                                         )
        health_snapshot.save()

    @property
    def gcs_total(self):
        if self.gcs_eye is None or self.gcs_verbal is None or self.gcs_motor is None:
            return 0
        return self.gcs_eye + self.gcs_verbal + self.gcs_motor


class NextOfKinContact(models.Model):

    class RelationshipChoices(models.TextChoices):
        WIFE = 'WIFE', 'Wife'
        HUSBAND = 'HUSBAND', 'Husband'
        CHILD = 'CHILD', 'Child'
        PARENT = 'PARENT', 'Parent'
        LEGAL_GUARDIAN = 'LEGAL GUARDIAN', 'Legal Guardian'
        OTHER = 'OTHER', 'Other'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE, related_name='next_of_kin_contacts')
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    title = models.CharField(max_length=20)
    relationship = models.CharField(max_length=20, choices=RelationshipChoices.choices)
    other_relationship = models.CharField(max_length=20, blank=True, null=True)
    phone_number = models.CharField(max_length=50)
    notes = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
