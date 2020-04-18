from django.contrib import admin

from django.db import models
from patient.models import Patient, PersonalData, Phone, \
    NextOfKinContact, PatientPhoto

from common.base_admin import SaveCurrentUser


class PatientInline(SaveCurrentUser, admin.TabularInline):
    model = Patient


class PersonalDataInline(SaveCurrentUser, admin.TabularInline):
    model = PersonalData


class PhoneInline(SaveCurrentUser, admin.TabularInline):
    model = Phone


class NextOfKinContactInline(SaveCurrentUser, admin.TabularInline):
    model = NextOfKinContact


class PatientPhotoInline(SaveCurrentUser, admin.TabularInline):
    model = PatientPhoto
    extra = 1
    min_num = 0
    max_num = 1


