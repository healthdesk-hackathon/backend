from rest_framework import serializers

from submission.models import Submission
from patient_tracker.models import Admission, HealthSnapshot


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
