from django.contrib import admin

from django.db import models
from patient.models import PersonalData, Phone, \
    NextOfKinContact, PatientPhoto


class PersonalDataInline(admin.TabularInline):
    model = PersonalData


class PhoneInline(admin.TabularInline):
    model = Phone


class NextOfKinContactInline(admin.TabularInline):
    model = NextOfKinContact


class PatientPhotoInline(admin.TabularInline):
    model = PatientPhoto
    extra = 1
    min_num = 0
    max_num = 1


