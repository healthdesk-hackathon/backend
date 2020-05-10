from django.contrib import admin
from workflow.models import Workflow


@admin.register(Workflow)
class WorkflowAdmin(admin.ModelAdmin):
    pass
