
import hashlib
import uuid

from django.db import transaction
from django.core.exceptions import ValidationError
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
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    local_barcode = models.CharField(max_length=150, unique=True)
    # submission = models.ForeignKey(Submission, on_delete=models.CASCADE, related_name='admissions', null=True)

    def assigned_bed(self):
        return self.assigned_beds.first()

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

    def validate_bed_type_available(bed_type):
        """before saving, if a bed type has been set, check that the requested bed type is available
        """
    
        if bed_type and not bed_type.is_available():
            raise ValidationError(
                'Bed type "%(value)s" is not available. Select another bed type, or add to the waiting list', 
                params={'value': bed_type.name}
            )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, validators=[prevent_update])
    admission = models.ForeignKey(Admission, on_delete=models.CASCADE, null=False, related_name='assigned_beds')
    bed_type = models.ForeignKey(BedType, validators=[validate_bed_type_available], on_delete=models.CASCADE, null=True, related_name='assigned_bed_types')
    waiting_for_bed_type = models.ForeignKey(BedType, on_delete=models.CASCADE, null=True, related_name='waiting_for_assigned_beds')
    waiting_since = models.DateTimeField(auto_now_add=True)


    def save(self):
        """override save to handle the (re)assignment of a patient to a bed
        """
        with transaction.atomic():
            # failsafe: check again that the bed is available, since we may not have a locking transaction in place yet
            if not self.bed_type.is_available():
                raise OperationalError('Bed type "%(value)s" is not available', params={'value': self.bed_type.name})

            # Does the current admission have an assigned bed already?
            if self.admission.assigned_bed:
                # Release the current bed and assign the new one
                self.leave_bed()
            
            # The bed assignment goes ahead through the creation of this record
            super(AssignedBed, self).save()
    
    def leave_bed(self):
        """The patient is leaving the bed. The current assignment to this patient can be removed.
        
        The bed must be taken out of service for cleaning.
        """

        with transaction.atomic():
            assigned_bed = self.admission.assigned_bed()
            if not assigned_bed:
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

