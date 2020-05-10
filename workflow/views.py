from django.shortcuts import render
from rest_framework import viewsets, permissions, mixins

from workflow.models import Workflow
from workflow.serializers import WorkflowSerializer

workflow_permissions = [permissions.DjangoModelPermissions]


class WorkflowViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Workflow.objects.all()
    serializer_class = WorkflowSerializer

    permission_classes = workflow_permissions

    def get_queryset(self):
        queryset = self.queryset
        patient_id = self.request.query_params.get('patient_id', None)
        workflow_type = self.request.query_params.get('workflow_type', None)

        conditions = {}
        if patient_id is not None:
            conditions['patient_id'] = patient_id

        if workflow_type is not None:
            conditions['workflow_type'] = workflow_type

        if len(conditions) > 0:
            queryset = queryset.filter(**conditions)

        return queryset

