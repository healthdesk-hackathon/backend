from django.db.models import Q, Count
from django.shortcuts import render

from rest_framework import viewsets, permissions, mixins
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from patient_tracker.serializers import *
from patient_tracker.models import *


patient_tracker_permissions = [permissions.DjangoModelPermissions]


class AdmissionViewSet(ModelViewSet):
    queryset = Admission.objects.all()
    serializer_class = AdmissionSerializer

    permission_classes = patient_tracker_permissions


class HealthSnapshotViewSet(ModelViewSet):
    queryset = HealthSnapshot.objects.all()
    serializer_class = HealthSnapshotSerializer

    permission_classes = patient_tracker_permissions

    def get_queryset(self):
        queryset = self.queryset
        admission_id = self.request.query_params.get('admission_id', None)

        if admission_id is not None:
            queryset = queryset.filter(admission=admission_id)

        return queryset


class DischargeViewSet(ModelViewSet):

    queryset = Discharge.objects.all()
    serializer_class = DischargeSerializer

    permission_classes = patient_tracker_permissions


class DeceasedViewSet(ModelViewSet):

    queryset = Deceased.objects.all()
    serializer_class = DeceasedSerializer

    permission_classes = patient_tracker_permissions


class OverallWellbeingViewSet(mixins.CreateModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):

    queryset = OverallWellbeing.objects.all()
    serializer_class = OverallWellbeingSerializer

    permission_classes = patient_tracker_permissions


class CommonSymptomsViewSet(mixins.CreateModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):

    queryset = CommonSymptoms.objects.all()
    serializer_class = CommonSymptomsSerializer

    permission_classes = patient_tracker_permissions


class GradedSymptomsViewSet(mixins.CreateModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):

    queryset = GradedSymptoms.objects.all()
    serializer_class = GradedSymptomsSerializer

    permission_classes = patient_tracker_permissions


class RelatedConditionsViewSet(mixins.CreateModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):

    queryset = RelatedConditions.objects.all()
    serializer_class = RelatedConditionsSerializer

    permission_classes = patient_tracker_permissions


