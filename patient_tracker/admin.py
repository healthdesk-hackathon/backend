from admin_actions.admin import ActionsModelAdmin
from django.contrib import admin

# Register your models here.
from django.shortcuts import redirect
from django.urls import reverse_lazy

from patient_tracker.models import Admission, Bed, BedType, BedAssignment
from submission.models import Patient, Submission
from django.utils.translation import gettext_lazy as _


class AdmissionInline(admin.TabularInline):
    model = Admission


@admin.register(BedType)
class BedTypeAdmin(admin.ModelAdmin):
    pass


@admin.register(Bed)
class BedsAdmin(ActionsModelAdmin):
    actions_row = ('set_to_available',)

    search_fields = [
        'id'
    ]

    list_display = (
        'id',
        'state',
        'reason',
        'bed_type'
    )

    list_filter = [
        'state',
        'reason',
        'bed_type__name'
    ]

    def set_to_available(self, request, pk):
        bed = Bed.objects.get(pk=pk)
        bed.state = Bed.StateChoices.AVAILABLE
        bed.save()
        return redirect(reverse_lazy('admin:patient_tracker_bed_changelist'))
    set_to_available.short_description = _('Set to available')
    set_to_available.url_path = 'set-available'


class AdmissionInline(admin.TabularInline):
    model = Admission


class SubmissionInline(admin.TabularInline):
    model = Submission
    show_change_link = True


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):

    inlines = [
        AdmissionInline,
        SubmissionInline
    ]


class AssignmentInline(admin.TabularInline):
    model = BedAssignment


@admin.register(Admission)
class AdmissionAdmin(admin.ModelAdmin):

    inlines = [
        AssignmentInline
    ]
