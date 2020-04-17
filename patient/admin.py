from django.contrib import admin

from django.db import models
from patient.models import Patient, PersonalData, Phone, \
    NextOfKinContact, PatientPhoto

from common.base_admin import SaveCurrentUser


class PatientInline(admin.TabularInline, SaveCurrentUser):
    model = Patient


class PersonalDataInline(admin.TabularInline, SaveCurrentUser):
    model = PersonalData


class PhoneInline(admin.TabularInline, SaveCurrentUser):
    model = Phone


class NextOfKinContactInline(admin.TabularInline, SaveCurrentUser):
    model = NextOfKinContact


class PatientPhotoInline(admin.TabularInline, SaveCurrentUser):
    model = PatientPhoto
    extra = 1
    min_num = 0
    max_num = 1


