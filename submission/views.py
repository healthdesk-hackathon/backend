from rest_framework import viewsets, permissions, mixins

from submission.models import Submission, PersonalData, Phone, OverallWellbeing, CommonSymptoms, \
    GradedSymptoms, RelatedConditions
from submission.serializers import SubmissionSerializer, PersonalDataSerializer, PhoneSerializer, \
    OverallWellbeingSerializer, CommonSymptomsSerializer, GradedSymptomsSerializer, RelatedConditionsSerializer


class SubmissionViewSet(mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin,
                        mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer

    permission_classes = [permissions.AllowAny]


class PersonalDataViewSet(mixins.CreateModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):

    queryset = PersonalData.objects.all()
    serializer_class = PersonalDataSerializer

    permission_classes = [permissions.AllowAny]


class PhoneViewSet(mixins.CreateModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):

    queryset = Phone.objects.all()
    serializer_class = PhoneSerializer

    permission_classes = [permissions.AllowAny]


class OverallWellbeingViewSet(mixins.CreateModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):

    queryset = OverallWellbeing.objects.all()
    serializer_class = OverallWellbeingSerializer

    permission_classes = [permissions.AllowAny]


class CommonSymptomsViewSet(mixins.CreateModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):

    queryset = CommonSymptoms.objects.all()
    serializer_class = CommonSymptomsSerializer

    permission_classes = [permissions.AllowAny]


class GradedSymptomsViewSet(mixins.CreateModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):

    queryset = GradedSymptoms.objects.all()
    serializer_class = GradedSymptomsSerializer

    permission_classes = [permissions.AllowAny]


class RelatedConditionsViewSet(mixins.CreateModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):

    queryset = RelatedConditions.objects.all()
    serializer_class = RelatedConditionsSerializer

    permission_classes = [permissions.AllowAny]
