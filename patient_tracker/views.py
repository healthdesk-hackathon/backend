from django.shortcuts import render

from rest_framework import viewsets, permissions, mixins

from patient_tracker.models import Admission, HealthSnapshot
from patient_tracker.serializers import AdmissionSerializer, HealthSnapshotSerializer


# Create your views here.
class AdmissionViewSet(mixins.CreateModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):

    queryset = Admission.objects.all()
    serializer_class = AdmissionSerializer

    permission_classes = [permissions.AllowAny]


class HealthSnapshotViewSet(mixins.CreateModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):

    queryset = HealthSnapshot.objects.all()
    serializer_class = HealthSnapshotSerializer

    permission_classes = [permissions.AllowAny]
