from django.shortcuts import render

from rest_framework import viewsets, permissions, mixins

from submission.models import Admission, Submission, PersonalData, Phone
from submission.serializers import AdmissionSerializer, SubmissionSerializer, PersonalDataSerializer, PhoneSerializer


class SubmissionViewSet(mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin,
                        viewsets.GenericViewSet):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer

    permission_classes = [permissions.AllowAny]


class AdmissionViewSet(mixins.CreateModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):

    queryset = Admission.objects.all()
    serializer_class = AdmissionSerializer

    permission_classes = [permissions.AllowAny]


class PersonalDataViewSet(mixins.CreateModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):

    queryset = PersonalData.objects.all()
    serializer_class = PersonalDataSerializer

    permission_classes = [permissions.AllowAny]


class PhoneViewSet(mixins.CreateModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):

    queryset = Phone.objects.all()
    serializer_class = PhoneSerializer

    permission_classes = [permissions.AllowAny]
