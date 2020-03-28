import hashlib
import uuid

from django.db import models


class Master(models.Model):
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
    master = models.ForeignKey(Master, on_delete=models.CASCADE, null=True, related_name='submissions')

    @property
    def patient_id(self):
        return hashlib.md5(self.id_type.encode() + self.identifier.encode()).digest()[:12]

    def save(self, **kwargs):
        if not self.master:
            patient_id = self.patient_id
            master, _ = Master.objects.get_or_create(anon_patient_id=patient_id)
            self.master = master
        super().save(**kwargs)


class Admission(models.Model):
    """
    Represents the admission into the hospital system, when the admins / triage have
    performed the initial steps for getting the patient into the system.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    local_barcode = models.CharField(max_length=150, unique=True)
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE, related_name='admissions')


class Person(models.Model):

    class GenderChoices(models.TextChoices):
        MALE = 'M', 'Male'
        FEMALE = 'F', 'Female'
        OTHER = 'O', 'Other/Prefer not to disclose'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE, related_name='persons')
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

