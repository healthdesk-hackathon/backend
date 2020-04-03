from rest_framework import serializers

from patient_tracker.models import Admission, HealthSnapshot, Bed, BedType


class AdmissionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Admission

        extra_kwargs = {'local_barcode': {'read_only': True}}

        fields = [
            'id',
            'local_barcode_image',
            'patient',
            'admitted'
        ]


class HealthSnapshotSerializer(serializers.ModelSerializer):

    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = HealthSnapshot
        extra_kwargs = {
            'created_at': { 'read_only': True }
        }
        fields = [
            'user',
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
