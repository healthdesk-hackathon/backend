from django.contrib import admin
import hashlib
import uuid

from django.db import models
from submission.models import Submission, Admission, PersonalData, Phone, OverallWellbeing, CommonSymptoms, \
    GradedSymptoms, RelatedConditions, MedicalCenter


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

class MedicalCenterAdmin(models.Model):
    model = MedicalCenter