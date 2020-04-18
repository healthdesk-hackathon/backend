from rest_framework import serializers

from patient.models import Patient
from patient_tracker.models import Admission, HealthSnapshot, \
    Discharge, Deceased, Patient, OverallWellbeing, CommonSymptoms, \
    GradedSymptoms, RelatedConditions

from patient.serializers import PatientSerializer

from common.base_serializers import ImmutableSerializerMeta


class AdmissionSerializer(serializers.ModelSerializer):

    current_bed = serializers.PrimaryKeyRelatedField(read_only=True)
    patient_id = serializers.PrimaryKeyRelatedField(source='patient', write_only=True, queryset=Patient.objects.all())

    class Meta:
        model = Admission

        extra_kwargs = {
            'patient_id': {'read_only': True},
            'local_barcode': {'read_only': True},
            'local_barcode_image': {'read_only': True},
            'patient': {'read_only': True},
            'admitted': {'read_only': True},
            'admitted_at': {'read_only': True},
            'current_severity': {'read_only': True},
            'current_bed': {'read_only': True},
            'patient_display': {'read_only': True},
        }

        patient = PatientSerializer()

        fields = ImmutableSerializerMeta.base_fields + [
            'local_barcode',
            'local_barcode_image',
            'patient',
            'patient_id',
            'admitted',
            'admitted_at',
            'current_severity',
            'current_bed',
            'patient_display'
        ]

        depth = 1


class HealthSnapshotSerializer(serializers.ModelSerializer):

    class Meta:
        model = HealthSnapshot

        fields = ImmutableSerializerMeta.base_fields + [
            'admission_id',

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


class DischargeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Discharge

        fields = ImmutableSerializerMeta.base_fields + [
            'admission_id',
            'discharged_at',
            'notes',
        ]


class DeceasedSerializer(serializers.ModelSerializer):

    class Meta:
        model = Deceased

        fields = ImmutableSerializerMeta.base_fields + [
            'admission_id',
            'registered_at',
            'notes',
        ]


class OverallWellbeingSerializer(serializers.ModelSerializer):
    class Meta:
        model = OverallWellbeing
        fields = ImmutableSerializerMeta.base_fields + [
            'admission_id',
            'overall_value',
        ]


class CommonSymptomsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommonSymptoms
        fields = ImmutableSerializerMeta.base_fields + [
            'admission_id',

            'chills',
            'achy_joints_muscles',
            'lost_taste_smell',
            'congestion',
            'stomach_disturbance',
            'tiredness',
            'headache',
            'dry_cough',
            'cough_with_sputum',
            'nauseous',
            'short_of_breath',
            'sore_throat',
            'fever',
            'runny_nose',
        ]


class GradedSymptomsSerializer(serializers.ModelSerializer):
    """
    Symptoms that a patient grades on a scale of 0 to 10
    """

    class Meta:
        model = GradedSymptoms
        fields = ImmutableSerializerMeta.base_fields + [
            'admission_id',

            'difficulty_breathing',
            'anxious'
        ]


class RelatedConditionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = RelatedConditions
        fields = ImmutableSerializerMeta.base_fields + [
            'admission_id',

            'heart_condition',
            'high_blood_pressure',
            'asthma',
            'chronic_lung_problems',
            'mild_diabetes',
            'chronic_diabetes',
            'current_chemo',
            'past_chemo',
            'take_immunosuppressants',
            'pregnant',
            'smoke'
        ]

