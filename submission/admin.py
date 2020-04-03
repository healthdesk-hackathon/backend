from django.contrib import admin

from django.db import models
from submission.models import Submission, PersonalData, Phone, OverallWellbeing, CommonSymptoms, \
    GradedSymptoms, RelatedConditions, ChosenMedicalCenter, MedicalCenter



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


class ChosenMedicalCenterInline(admin.TabularInline):
    model = ChosenMedicalCenter


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):

    inlines = [
        PhoneInline,
        PersonalDataInline,
        OverallWellbeingInline,
        CommonSymptomsInline,
        GradedSymptomsInline,
        RelatedConditionsInline,
        ChosenMedicalCenterInline
    ]


class MedicalCenterAdmin(models.Model):
    model = MedicalCenter
