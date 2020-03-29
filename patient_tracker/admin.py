from admin_actions.admin import ActionsModelAdmin
from django.contrib import admin, messages
from django.core.exceptions import ValidationError

from django.shortcuts import redirect
from django.urls import reverse_lazy

from patient_tracker.models import Admission, Bed, BedType, BedAssignment, HealthSnapshot
from project.admin import admin_site
from submission.models import Patient, Submission
from django.utils.translation import gettext_lazy as _


class AdmissionInline(admin.TabularInline):
    model = Admission


@admin.register(BedType, site=admin_site)
class BedTypeAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'total',
        'number_available',
        'number_assigned',
        'number_out_of_service',
    ]


@admin.register(Bed, site=admin_site)
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

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False

    # def delete_model(self, request, obj):
    #     try:
    #         super().delete_model(request, obj)
    #     except ValidationError as e:
    #         messages.error(request, str(e))

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


@admin.register(Patient, site=admin_site)
class PatientAdmin(admin.ModelAdmin):
    inlines = [
        AdmissionInline,
        SubmissionInline
    ]


class AssignmentInline(admin.TabularInline):
    model = BedAssignment
    extra = 0

    can_delete = False

    fields = [
        'bed',
        'assigned_at',
        'unassigned_at'
    ]

    readonly_fields = fields


class HealthSnapshotInline(admin.TabularInline):
    model = HealthSnapshot
    extra = 0
    fields = [
        'blood_pressure_systolic',
        'blood_pressure_diastolic',
        'heart_rate',
        'breathing_rate',
        'temperature',
        'oxygen_saturation',

        'gcs_eye',
        'gcs_verbal',
        'gcs_motor',

        'observations',

        'severity',
    ]

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Admission, site=admin_site)
class AdmissionAdmin(ActionsModelAdmin):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        actions_details = (
            'discharge_patient',
        )

        for bed_type in BedType.objects.all():
            action_slug = '-'.join(bed_type.name.lower().split(' '))
            action = lambda request, pk, bed_type=bed_type: self.bed_type_dispatch_action(request, pk, bed_type)
            setattr(action, 'short_description', f'Assign to bed: {bed_type.name}')
            setattr(action, 'url_path', f'set-{action_slug}')

            action_name = f'assign_to_{action_slug.replace("-", "_")}'
            setattr(self, action_name, action)
            actions_details += (action_name,)

        setattr(self, 'actions_detail', actions_details)

    fields = [
        'local_barcode',
        'current_severity',
        'is_discharged',
        'current_bed'
    ]

    search_fields = [
        'local_barcode',
    ]

    readonly_fields = fields

    inlines = [
        HealthSnapshotInline,
        AssignmentInline
    ]

    date_hierarchy = 'admitted_at'

    list_display = [
        'local_barcode',
        'patient',
        'admitted_at',
        'discharged',
        'current_severity'
    ]

    list_filter = [
        'admitted_at'
    ]

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False

    def bed_type_dispatch_action(self, request, pk, bed_type):
        admission = Admission.objects.get(pk=pk)
        try:
            admission.assign_bed(bed_type)
            messages.success(request, 'Person successfuly moved to another bed')
        except Bed.DoesNotExist as e:
            messages.error(request, str(e))
        return redirect(reverse_lazy('admin:patient_tracker_admission_changelist'))

    def discharge_patient(self, request, pk):
        admission = Admission.objects.get(pk=pk)
        admission.discharge()
        messages.success(request, 'Person has been successfully discharged')
        return redirect(reverse_lazy('admin:patient_tracker_admission_changelist'))

    discharge_patient.url_path = 'discharge'
    discharge_patient.short_description = 'Discharge'


class HealthSnapshotProxy(HealthSnapshot):
    class Meta:
        verbose_name = 'Health Snapshot'
        proxy = True


@admin.register(HealthSnapshotProxy, site=admin_site)
class HealthSnapshotAdmin(ActionsModelAdmin):
    actions_row = ('go_to_admission',)

    date_hierarchy = 'created_at'

    list_filter = [
        'severity'
    ]

    list_display = (
        'severity',
        'blood_pressure_systolic',
        'blood_pressure_diastolic',
        'heart_rate',
        'breathing_rate',
        'temperature',
        'oxygen_saturation',
        'gcs_total'
    )

    list_display_links = []

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def go_to_admission(self, request, pk):
        snapshot = HealthSnapshot.objects.get(pk=pk)
        return redirect(
            reverse_lazy('admin:patient_tracker_admission_change', kwargs={'object_id': snapshot.admission.pk}))

    go_to_admission.short_description = _('Go to admission')
    go_to_admission.url_path = 'go-to-admission'
