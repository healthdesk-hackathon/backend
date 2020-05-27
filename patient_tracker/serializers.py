from rest_framework import serializers

from patient.models import Patient
from patient_tracker.models import Admission, HealthSnapshot, \
    Discharge, Deceased, OverallWellbeing, CommonSymptoms, \
    GradedSymptoms, RelatedConditions

from patient.serializers import PatientSerializer

from common.base_serializers import ImmutableSerializerMeta, CurrentSerializerMeta, BaseSaveSerializer


class AdmissionSerializer(BaseSaveSerializer, serializers.ModelSerializer):

    current_bed=serializers.PrimaryKeyRelatedField(read_only=True)
    patient_id=serializers.PrimaryKeyRelatedField(source='patient', write_only=True, queryset=Patient.objects.all())

    class Meta:
        model=Admission

        extra_kwargs={
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

        fields = CurrentSerializerMeta.base_fields + [
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
        read_only_fields = CurrentSerializerMeta.read_only_fields

        depth = 1


class HealthSnapshotSerializer(BaseSaveSerializer, serializers.ModelSerializer):
    admission_id=serializers.PrimaryKeyRelatedField(
        source='admission', write_only=True, queryset=Admission.objects.all())

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
            'main_complain',
            'gcs_eye',
            'gcs_verbal',
            'gcs_motor',
            'observations',
            'severity',
        ]
        read_only_fields = ImmutableSerializerMeta.read_only_fields


class DischargeSerializer(BaseSaveSerializer, serializers.ModelSerializer):
    admission_id=serializers.PrimaryKeyRelatedField(
        source='admission', write_only=True, queryset=Admission.objects.all())

    class Meta:
        model = Discharge

        fields = ImmutableSerializerMeta.base_fields + [
            'admission_id',
            'discharged_at',
            'notes',
        ]
        read_only_fields = ImmutableSerializerMeta.read_only_fields


class DeceasedSerializer(BaseSaveSerializer, serializers.ModelSerializer):
    admission_id=serializers.PrimaryKeyRelatedField(
        source='admission', write_only=True, queryset=Admission.objects.all())

    class Meta:
        model = Deceased

        fields = ImmutableSerializerMeta.base_fields + [
            'admission_id',
            'registered_at',
            'notes',
        ]
        read_only_fields = ImmutableSerializerMeta.read_only_fields


class OverallWellbeingSerializer(BaseSaveSerializer, serializers.ModelSerializer):
    admission_id=serializers.PrimaryKeyRelatedField(
        source='admission', write_only=True, queryset=Admission.objects.all())

    class Meta:
        model = OverallWellbeing
        fields = ImmutableSerializerMeta.base_fields + [
            'admission_id',
            'overall_value',
        ]
        read_only_fields = ImmutableSerializerMeta.read_only_fields


class CommonSymptomsSerializer(BaseSaveSerializer, serializers.ModelSerializer):

    admission_id=serializers.PrimaryKeyRelatedField(
        source='admission', write_only=True, queryset=Admission.objects.all())

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
        read_only_fields = ImmutableSerializerMeta.read_only_fields


class GradedSymptomsSerializer(BaseSaveSerializer, serializers.ModelSerializer):
    """
    Symptoms that a patient grades on a scale of 0 to 10
    """
    admission_id=serializers.PrimaryKeyRelatedField(
        source='admission', write_only=True, queryset=Admission.objects.all())

    class Meta:
        model = GradedSymptoms
        fields = ImmutableSerializerMeta.base_fields + [
            'admission_id',

            'difficulty_breathing',
            'anxious'
        ]
        read_only_fields = ImmutableSerializerMeta.read_only_fields


class RelatedConditionsSerializer(BaseSaveSerializer, serializers.ModelSerializer):
    admission_id=serializers.PrimaryKeyRelatedField(
        source='admission', write_only=True, queryset=Admission.objects.all())

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
        read_only_fields = ImmutableSerializerMeta.read_only_fields

