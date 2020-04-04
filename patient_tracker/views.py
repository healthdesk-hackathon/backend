from django.shortcuts import render

from rest_framework import viewsets, permissions, mixins
from rest_framework.viewsets import ModelViewSet

from patient_tracker.models import Admission, HealthSnapshot, Bed, BedType
from patient_tracker.serializers import AdmissionSerializer, HealthSnapshotSerializer, BedSerializer, BedTypeSerializer


# Create your views here.
class AdmissionViewSet(mixins.CreateModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):

    queryset = Admission.objects.all()
    serializer_class = AdmissionSerializer

    permission_classes = [permissions.AllowAny]


class HealthSnapshotViewSet(mixins.CreateModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):

    queryset = HealthSnapshot.objects.all()
    serializer_class = HealthSnapshotSerializer

    permission_classes = [permissions.AllowAny]


class BedViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):

    queryset = Bed.objects.all()
    serializer_class = BedSerializer

    permission_classes = [permissions.DjangoModelPermissions]


class BedTypeViewSet(ModelViewSet):

    queryset = BedType.objects.all()
    serializer_class = BedTypeSerializer

    permission_classes = [permissions.DjangoModelPermissions]
