from admin_actions.admin import ActionsModelAdmin
from django.contrib import admin, messages

from django.shortcuts import redirect
from django.urls import reverse_lazy

from equipment.models import *
from project.admin import admin_site
from django.utils.translation import gettext_lazy as _


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

