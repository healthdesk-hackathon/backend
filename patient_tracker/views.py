from django.db.models import Q, Count
from django.shortcuts import render
from drf_yasg.utils import swagger_auto_schema

from rest_framework import viewsets, permissions, mixins
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from patient_tracker.models import Admission, HealthSnapshot, Bed, BedType, Discharge, Deceased, BedAssignment
from patient_tracker.serializers import AdmissionSerializer, HealthSnapshotSerializer, BedSerializer, BedTypeSerializer, \
    DischargeSerializer, DeceasedSerializer, DashboardSerializer


class AdmissionViewSet(ModelViewSet):
    queryset = Admission.objects.all()
    serializer_class = AdmissionSerializer

    permission_classes = [permissions.DjangoModelPermissions]


class HealthSnapshotViewSet(ModelViewSet):
    queryset = HealthSnapshot.objects.all()
    serializer_class = HealthSnapshotSerializer

    permission_classes = [permissions.DjangoModelPermissions]


class BedViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    queryset = Bed.objects.all()
    serializer_class = BedSerializer

    permission_classes = [permissions.DjangoModelPermissions]


class BedTypeViewSet(ModelViewSet):
    queryset = BedType.objects.all()
    serializer_class = BedTypeSerializer

    permission_classes = [permissions.DjangoModelPermissions]


class DashboardView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_data(self):
        data = {
            'bed_availability': [],
            'global_availability': 0,
            'total_discharges': 0,
            'assignments': [],
            'admissions_per_day': [],
            'average_duration': None
        }

        bed_types = BedType.objects.all()
        for bt in bed_types:
            bt: BedType
            available_beds_ratio = (1 / bt.beds.count()) * bt.number_available if bt.beds.count() > 0 else 1
            data['bed_availability'].append({'label': bt.name, 'value': available_beds_ratio})

        total_beds = Bed.objects.count()
        total_available = 1 / total_beds * Bed.objects.available().count() if total_beds > 0 else 1

        data['global_availability'] = total_available
        data['total_discharges'] = Discharge.objects.count()

        data['assignments'] = list(BedAssignment.objects.current_per_severity())

        duration = Admission.objects.average_duration()
        data['average_duration'] = duration

        admissions_per_day = Admission.objects.admissions_per_day()
        data['admissions_per_day'] = admissions_per_day

        return data

    @swagger_auto_schema(
        operation_description="Returns read only global metrics",
        responses={200: DashboardSerializer()}
    )
    def get(self, request):
        serializer = DashboardSerializer(data=self.get_data())
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data)


class DischargeViewSet(ModelViewSet):

    queryset = Discharge.objects.all()
    serializer_class = DischargeSerializer

    permission_classes = [permissions.DjangoModelPermissions]


class DeceasedViewSet(ModelViewSet):

    queryset = Deceased.objects.all()
    serializer_class = DeceasedSerializer

    permission_classes = [permissions.DjangoModelPermissions]
