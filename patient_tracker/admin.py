from django.contrib import admin

# Register your models here.
from patient_tracker.models import Admission


class AdmissionInline(admin.TabularInline):
    model = Admission

# TODO register something here?
#@admin.register(Patient)
class PatientTrackerAdmin(admin.ModelAdmin):

    inlines = [
        AdmissionInline
    ]
