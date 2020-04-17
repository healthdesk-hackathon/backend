import hashlib

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from common.base_models import ImmutableBaseModel, CurrentBaseModel


class Patient(CurrentBaseModel):
    """
    Patient record, ties all patient related info together.
    """

    identifier = models.CharField(max_length=50, null=False)
    id_type = models.CharField(max_length=50, null=False)

    class Meta:
        ordering = ['-created']

    @property
    def patient_anon_id(self):
        return hashlib.md5(self.id_type.encode() + self.identifier.encode()).hexdigest()[:12]

    @property
    def current_admission(self):
        admission = self.admissions.first()
        return admission


class PersonalData(CurrentBaseModel):
    class GenderChoices(models.TextChoices):
        MALE = 'M', 'Male'
        FEMALE = 'F', 'Female'
        OTHER = 'O', 'Other/Prefer not to disclose'

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='personal_data')
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    gender = models.CharField(max_length=1, choices=GenderChoices.choices)
    date_of_birth = models.DateField(auto_now=False, auto_now_add=False)


class Phone(CurrentBaseModel):
    """
    Represents a phone number to be used identification or contact with the person
    phone type: mobile, home, work
    """

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='phones')
    phone_number = models.CharField(max_length=50)
    phone_type = models.CharField(max_length=10)


class NextOfKinContact(CurrentBaseModel):

    class RelationshipChoices(models.TextChoices):
        WIFE = 'WIFE', 'Wife'
        HUSBAND = 'HUSBAND', 'Husband'
        CHILD = 'CHILD', 'Child'
        PARENT = 'PARENT', 'Parent'
        LEGAL_GUARDIAN = 'LEGAL GUARDIAN', 'Legal Guardian'
        OTHER = 'OTHER', 'Other'

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='next_of_kin_contacts')
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    title = models.CharField(max_length=20)
    relationship = models.CharField(max_length=20, choices=RelationshipChoices.choices)
    other_relationship = models.CharField(max_length=20, blank=True, null=True)
    phone_number = models.CharField(max_length=50)
    notes = models.TextField()


class PatientPhoto(CurrentBaseModel):
    image_path = 'patient_photos'

    patient = models.OneToOneField(Patient, on_delete=models.CASCADE, related_name='patient_photo')
    photo = models.ImageField(upload_to=image_path)
