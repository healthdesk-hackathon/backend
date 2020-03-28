from django.contrib import admin
import hashlib
import uuid

from django.db import models
from submission.models import Submission, Admission, PersonalData, Phone, OverallWellbeing, CommonSymptoms, \
    GradedSymptoms, RelatedConditions

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


class AdmissionInline(admin.TabularInline):
    model = Admission


class PersonalDataInline(admin.TabularInline):
    model = PersonalData


class PhoneInline(admin.TabularInline):
    model = Phone


class OverallWellbeingInline(admin.TabularInline):
    model = OverallWellbeing


class CommonSymptomsInline(admin.TabularInline):
    model = CommonSymptoms


class GradedSymptomsInline(admin.TabularInline):
    model = GradedSymptoms


class RelatedConditionsInline(admin.TabularInline):
    model = RelatedConditions


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):

    inlines = [
        AdmissionInline,
        PhoneInline,
        PersonalDataInline,
        OverallWellbeingInline,
        CommonSymptomsInline,
        GradedSymptomsInline,
        RelatedConditionsInline
    ]
