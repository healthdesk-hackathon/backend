import hashlib
import uuid

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from submission.admin import MedicalCenter

class Patient(models.Model):
    """
    Central crosswalk model to connect all related records for a unique patient
    """

    anon_patient_id = models.CharField(max_length=12, default=None, unique=True)


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
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True, related_name='submissions')

    @property
    def patient_anon_id(self):
        return hashlib.md5(self.id_type.encode() + self.identifier.encode()).digest()[:12]

    def save(self, **kwargs):
        if not self.master:
            patient_id = self.patient_anon_id
            patient, _ = Patient.objects.get_or_create(anon_patient_id=patient_id)
            self.patient = patient
        super().save(**kwargs)


class Admission(models.Model):
    """
    Represents the admission into the hospital system, when the admins / triage have
    performed the initial steps for getting the patient into the system.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    local_barcode = models.CharField(max_length=150, unique=True)
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE, related_name='admissions')


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


class ChosenMedicalCenter(models.Model):
    """
    The patient has selected a preferred medical center. Record this selection
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    submission = models.OneToOneField(Submission, on_delete=models.CASCADE, related_name='chosen_medical_center')

    medical_center = models.ForeignKey(MedicalCenter, on_delete=models.CASCADE, related_name='medical_center')
    
