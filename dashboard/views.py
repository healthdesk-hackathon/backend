from django.shortcuts import render
from rest_framework import viewsets, permissions
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema

from dashboard.serializers import DashboardSerializer

dashboard_permissions = [permissions.IsAuthenticated]


class DashboardView(APIView):
    permission_classes = dashboard_permissions

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

