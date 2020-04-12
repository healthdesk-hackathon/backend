import os
import string

from common.base_models import ImmutableBaseModel, CurrentBaseModel
from django.conf import settings
from django.core.files.images import ImageFile
from django.db import transaction
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Count, F, Avg, Subquery, OuterRef, Max
from django.utils import timezone as tz

# from patient_tracker.models import Admission, BedAssignment


class Bed(CurrentBaseModel):
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

    # admissions = models.ManyToManyField(Admission, through=BedAssignment, related_name='assigned_beds')

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


class BedType(CurrentBaseModel):
    """The numbers of each type of bed that a hospital has as resources.

    We want a manager to be able to view the number of beds of each type / number occupied /
    number out of service (cleaning)

    """

    class SeverityMatchChoices(models.TextChoices):
        RED = 'RED', 'Red'
        YELLOW = 'YELLOW', 'Yellow'
        GREEN = 'GREEN', 'Green'

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

