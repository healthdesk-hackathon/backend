from admin_actions.admin import ActionsModelAdmin
from django.contrib import admin, messages

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
    actions_row = (
        'set_to_available',
        'set_to_equipment_failure',
        'set_to_unavailable',
        'set_to_cleaning'
    )


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
    set_to_available.short_description = _('Available')
    set_to_available.url_path = 'set-available'

    def set_to_equipment_failure(self, request, pk):
        bed = Bed.objects.get(pk=pk)
        bed.state = Bed.StateChoices.OUT_OF_SERVICE
        bed.reason = Bed.ReasonChoices.EQUIP_FAIL
        bed.save()
        return redirect(reverse_lazy('admin:patient_tracker_bed_changelist'))
    set_to_equipment_failure.short_description = _('Equipment failed')
    set_to_equipment_failure.url_path = 'set-equip-fail'

    def set_to_unavailable(self, request, pk):
        bed = Bed.objects.get(pk=pk)
        bed.state = Bed.StateChoices.OUT_OF_SERVICE
        bed.reason = Bed.ReasonChoices.UNAVAILABLE
        bed.save()
        return redirect(reverse_lazy('admin:patient_tracker_bed_changelist'))
    set_to_unavailable.short_description = _('Unavailable')
    set_to_unavailable.url_path = 'set-unavailable'

    def set_to_cleaning(self, request, pk):
        bed = Bed.objects.get(pk=pk)
        bed.state = Bed.StateChoices.OUT_OF_SERVICE
        bed.reason = Bed.ReasonChoices.CLEANING
        bed.save()
        return redirect(reverse_lazy('admin:patient_tracker_bed_changelist'))
    set_to_cleaning.short_description = _('Cleaning required')
    set_to_cleaning.url_path = 'set-cleaning'


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

    extra = 0


@admin.register(Admission)
class AdmissionAdmin(ActionsModelAdmin):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        actions_details = ()

        for bed_type in BedType.objects.all():

            action_slug = '-'.join(bed_type.name.lower().split(' '))
            action = lambda request, pk, bed_type=bed_type: self.bed_type_dispatch_action(request, pk, bed_type)
            setattr(action, 'short_description', f'Assign to bed: {bed_type.name}')
            setattr(action, 'url_path', f'set-{action_slug}')

            action_name = f'assign_to_{action_slug.replace("-", "_")}'
            setattr(self, action_name, action)
            actions_details += (action_name,)

        setattr(self, 'actions_detail', actions_details)

    inlines = [
        AssignmentInline
    ]

    def bed_type_dispatch_action(self, request, pk, bed_type):
        admission = Admission.objects.get(pk=pk)
        try:
            admission.assign_bed(bed_type)
            messages.success(request, 'Person successfuly moved to another bed')
        except Bed.DoesNotExist as e:
            messages.error(request, str(e))
        return redirect(reverse_lazy('admin:patient_tracker_admission_changelist'))
