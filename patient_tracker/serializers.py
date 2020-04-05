from rest_framework import serializers

from submission.serializers import *
from patient_tracker.models import Admission, HealthSnapshot, Bed, BedType, \
    Discharge, Deceased, Patient


class PatientSerializer(serializers.ModelSerializer):
    submissions = SubmissionSerializer(many=True, read_only=True)

    class Meta:
        model = Patient
        fields = [
            'id',
            'anon_patient_id',
            'submissions'
        ]


class AdmissionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Admission

        extra_kwargs = {
            'local_barcode': {'read_only': True},
            'local_barcode_image': {'read_only': True},
            'patient': {'read_only': True},
            'admitted': {'read_only': True},
            'admitted_at': {'read_only': True},
            'current_severity': {'read_only': True},
            'current_bed': {'read_only': True},
        }

        patient = PatientSerializer()

        fields = [
            'id',
            'local_barcode',
            'local_barcode_image',
            'patient',
            'admitted',
            'admitted_at',
            'current_severity',
            'current_bed',
        ]

        depth = 1


class HealthSnapshotSerializer(serializers.ModelSerializer):

    # user = serializers.HiddenField(
    #     default=serializers.CurrentUserDefault()
    # )

    class Meta:
        model = HealthSnapshot
        extra_kwargs = {
            'created_at': {'read_only': True}
        }
        fields = [
            # 'user',
            'created_at',
            'admission',

            'blood_pressure_systolic',
            'blood_pressure_diastolic',
            'heart_rate',
            'breathing_rate',
            'temperature',
            'oxygen_saturation',

            'gcs_eye',
            'gcs_verbal',
            'gcs_motor',

            'observations',

            'severity',
        ]


class BedSerializer(serializers.ModelSerializer):

    current_admission = AdmissionSerializer(read_only=True)

    class Meta:
        model = Bed
        fields = [
            'id',
            'bed_type',
            'admissions',
            'reason',
            'state',
            'bed_type',
            'current_admission'
        ]


class BedTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = BedType
        extra_kwargs = {
            'number_out_of_service': {'read_only': True},
            'number_assigned': {'read_only': True},
            'number_available': {'read_only': True},
            'number_waiting': {'read_only': True},
            'is_available': {'read_only': True},
        }
        fields = [
            'id',
            'name',
            'total',

            'number_out_of_service',
            'number_assigned',
            'number_available',
            'number_waiting',
            'is_available',
        ]


class LabelledValueSerializer(serializers.Serializer):
    label = serializers.CharField()
    value = serializers.FloatField()


class AdmissionCountSerializer(serializers.Serializer):

    date = serializers.DateField()
    count = LabelledValueSerializer(many=True)


class DashboardSerializer(serializers.Serializer):
    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    bed_availability = LabelledValueSerializer(many=True)
    assignments = LabelledValueSerializer(many=True)
    global_availability = serializers.FloatField()
    total_discharges = serializers.IntegerField()
    average_duration = serializers.DurationField()
    admissions_per_day = AdmissionCountSerializer(many=True)

    class Meta:
        fields = [
            'bed_availability',
            'global_availability',
            'total_discharges',
            'assignments'
        ]


class DischargeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Discharge

        fields = [
            'id',
            'admission',
            'discharged_at',
            'notes',
            'user',
        ]


class DeceasedSerializer(serializers.ModelSerializer):

    class Meta:
        model = Deceased

        fields = [
            'id',
            'admission',
            'created_at',
            'registered_at',
            'notes',
            'registered_at',
            'user'
        ]
