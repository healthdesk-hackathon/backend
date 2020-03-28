
import hashlib
import uuid

from django.db import transaction
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.core import validators
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver

from submission.models import Submission


def prevent_update(pk):
    """prevent a record from being saved if it has a pk
    """

    if pk:
        raise ValidationError(
            'record must not be updated'
        )


class Admission(models.Model):
    """
    Represents the admission into the hospital system, when the admins / triage have
    performed the initial steps for getting the patient into the system.

    This class not only represents the action of admission, but also the person as they move 
    around inside the hospital system. This saves us having to reference up to the 'Patient'
    record, the parent of this.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    local_barcode = models.CharField(max_length=150, unique=True, null=True)
    # submission = models.ForeignKey(Submission, on_delete=models.CASCADE, related_name='admissions', null=True)
    admitted_at = models.DateTimeField(auto_now_add=True)

    def current_bed(self):
        return self.assigned_beds.first()

    def assign_bed(self, bed_type):
        new_bed = AssignedBed(admission = self, bed_type=bed_type)
        new_bed.save()
        return new_bed


class Discharge(models.Model):
    """
    Represents the discharge from the hospital system, when the admins / triage have
    completed any steps to release them.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # submission = models.ForeignKey(Submission, on_delete=models.CASCADE, related_name='admissions', null=True)
    discharged_at = models.DateTimeField(auto_now_add=True)


class BedType(models.Model):
    """The numbers of each type of bed that a hospital has as resources.

    We want a manager to be able to view the number of beds of each type / number occupied / 
    number out of service (cleaning)
 
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50, blank=False)
    total = models.IntegerField(null=False)

    def number_out_of_service(self):
        return self.out_of_service_beds.count()

    def number_assigned(self):
        return self.assigned_bed_types.count()

    def number_available(self):
        used = self.number_assigned() + self.number_out_of_service()
        available = self.total - used
        return available

    def number_waiting(self):
        return self.waiting_for_assigned_beds.count()

    def is_available(self):
        """Check if this bed type is available for a new patient
        """
        return self.number_available() > 0
        

class Bed(models.Model):
    """
    Individual bed resources that can be assigned to a patient.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    bed_type = models.ForeignKey(BedType, on_delete=models.CASCADE, null=False, related_name='beds')


class AssignedBed(models.Model):
    """
    By assigning a new bed to a patient, we must choose the type of bed that is required.

    This class provides the logic to check if a bed of a specific type is available for 
    assignment to a patient, and to assign it. 
    

    On create, check if there is a bed of the appropriate type in the pool of available beds:

    yes: take the bed out of the pool of available beds and assign it to the patient. The patient can be moved
    no: suggest the next best available bed for them. Repeat the submission.
    
    If there are no possible options for a bed assignment, allow the user to add them to a waiting list.

    If a patient is currently in a bed and is assigned a new one, we must take the current bed out of service (for cleaning),
    so that it can not be automatically taken by another patient until it is ready.

    TODO - everything here must be handled through a locked transaction,
    to prevent race conditions from assigning a single bed to two patients.
    """


    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, validators=[prevent_update])
    admission = models.ForeignKey(Admission, on_delete=models.CASCADE, null=False, related_name='assigned_beds')
    bed_type = models.ForeignKey(BedType, on_delete=models.CASCADE, null=True, related_name='assigned_bed_types')
    waiting_for_bed_type = models.ForeignKey(BedType, on_delete=models.CASCADE, null=True, related_name='waiting_for_assigned_beds')
    waiting_since = models.DateTimeField(auto_now_add=True)


    def save(self):
        """override save to handle the (re)assignment of a patient to a bed
        """
        with transaction.atomic():
            # check that the bed is available. A validator on the foreign key field doesn't seem to work
            if not self.bed_type.is_available():
                raise ObjectDoesNotExist('Bed type is not available')

            # Does the current admission have an assigned bed already?
            if self.id and self.admission.current_bed():
                # Release the current bed and assign the new one
                self.leave_bed()
            
            # The bed assignment goes ahead through the creation of this record
            super(AssignedBed, self).save()
    
    def leave_bed(self):
        """The patient is leaving the bed. The current assignment to this patient can be removed.
        
        The bed must be taken out of service for cleaning.
        """

        with transaction.atomic():

            assigned_bed = self.admission.current_bed()

            if not assigned_bed or assigned_bed.id == self.id:
                return  

            bed_type = assigned_bed.bed_type

            OutOfServiceBed.objects.create(bed_type=bed_type, reason=OutOfServiceBed.ReasonChoices.CLEANING)
            assigned_bed.delete()



class OutOfServiceBed(models.Model):
    """Take a bed out of service, for cleaning or other reason (broken equipment, etc)
    """

    class ReasonChoices(models.TextChoices):
        CLEANING = 'cleaning', 'cleaning'
        EQUIP_FAIL = 'equip fail', 'equipment failure'
        UNAVAILABLE = 'unavailable', 'unavailable'
        OTHER = 'other', 'other'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    bed_type = models.ForeignKey(BedType, on_delete=models.CASCADE, null=True, related_name='out_of_service_beds')
    when_out_of_service = models.DateTimeField(auto_now_add=True)
    reason = models.CharField(max_length=20, choices=ReasonChoices.choices)

    def put_back_in_service(self):
        """Return this bed to service"""
        self.delete()
