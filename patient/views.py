from rest_framework import viewsets, permissions, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from patient.models import Patient, PersonalData, NextOfKinContact, Phone, PatientIdentifier
from patient.serializers import PatientSerializer, PersonalDataSerializer, \
    PatientIdentifierSerializer, PhoneSerializer, NextOfKinContactSerializer


patient_permissions = [permissions.DjangoModelPermissions]


class PatientViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):

    queryset = Patient.objects.all()
    serializer_class = PatientSerializer

    permission_classes = patient_permissions

    @action(detail=False, methods=["post"])
    def start_new_patient_admission(self, request):
        patient = Patient.PatientManager.start_new_patient_admission(current_user=request.user)
        serializer = self.get_serializer(patient)
        return Response(serializer.data)


class PatientIdentifierDataViewSet(mixins.CreateModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):

    queryset = PatientIdentifier.objects.all()
    serializer_class = PatientIdentifierSerializer

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
