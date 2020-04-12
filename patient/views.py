from rest_framework import viewsets, permissions, mixins

from patient.models import *
from patient.serializers import *


patient_permissions = [permissions.DjangoModelPermissions]


class PatientViewSet(mixins.CreateModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):

    queryset = Patient.objects.all()
    serializer_class = PatientSerializer

    permission_classes = patient_permissions


class PersonalDataViewSet(mixins.CreateModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):

    queryset = PersonalData.objects.all()
    serializer_class = PersonalDataSerializer

    permission_classes = patient_permissions


class PhoneViewSet(mixins.CreateModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):

    queryset = Phone.objects.all()
    serializer_class = PhoneSerializer

    permission_classes = patient_permissions


class NextOfKinContactViewSet(mixins.CreateModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    queryset = NextOfKinContact.objects.all()
    serializer_class = NextOfKinContactSerializer

    permission_classes = patient_permissions
