from django.contrib import admin
from dummy.models import Dummy


@admin.register(Dummy)
class DummyAdmin(admin.ModelAdmin):
    pass
