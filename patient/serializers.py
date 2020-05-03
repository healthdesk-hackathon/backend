from rest_framework import serializers

from patient.models import Patient, PatientIdentifier, PersonalData, NextOfKinContact, Phone
from common.base_serializers import ImmutableSerializerMeta, CurrentSerializerMeta, BaseSaveSerializer


class PatientSerializer(BaseSaveSerializer, serializers.ModelSerializer):

    class Meta:
        model = Patient

        extra_kwargs={
            'current_admission_id': {'read_only': True},
            'personal_data': {'read_only': True},
            'patient_identifiers': {'read_only': True},
            'phones': {'read_only': True},
            'next_of_kin_contacts': {'read_only': True}
        }

        fields = ImmutableSerializerMeta.base_fields + [
            'current_admission_id',
            'personal_data',
            'patient_identifiers',
            'phones',
            'next_of_kin_contacts'
        ]
        read_only_fields=ImmutableSerializerMeta.read_only_fields

        depth = 1


class PatientIdentifierSerializer(BaseSaveSerializer, serializers.ModelSerializer):

    patient_id=serializers.PrimaryKeyRelatedField(source='patient', write_only=True, queryset=Patient.objects.all())

    class Meta:
        model=PatientIdentifier
        fields=CurrentSerializerMeta.base_fields + [
            'patient_id',
            'identifier',
            'id_type'
        ]
        read_only_fields=CurrentSerializerMeta.read_only_fields


class PersonalDataSerializer(BaseSaveSerializer, serializers.ModelSerializer):

    patient_id=serializers.PrimaryKeyRelatedField(source='patient', write_only=True, queryset=Patient.objects.all())

    class Meta:
        model=PersonalData
        fields=CurrentSerializerMeta.base_fields + [
            'patient_id',
            'first_name',
            'last_name',
            'gender',
            'date_of_birth',
        ]

        read_only_fields=CurrentSerializerMeta.read_only_fields


class PhoneSerializer(BaseSaveSerializer, serializers.ModelSerializer):

    patient_id=serializers.PrimaryKeyRelatedField(source='patient', write_only=True, queryset=Patient.objects.all())

    class Meta:
        model=Phone
        fields=CurrentSerializerMeta.base_fields + [
            'patient_id',
            'phone_number',
            'phone_type',
        ]
        read_only_fields=CurrentSerializerMeta.read_only_fields


class NextOfKinContactSerializer(BaseSaveSerializer, serializers.ModelSerializer):

    patient_id=serializers.PrimaryKeyRelatedField(source='patient', write_only=True, queryset=Patient.objects.all())

    class Meta:
        model=NextOfKinContact

        fields=CurrentSerializerMeta.base_fields + [
            'patient_id',
            'first_name',
            'last_name',
            'title',
            'relationship',
            'other_relationship',
            'phone_number',
            'notes',
        ]
        read_only_fields=CurrentSerializerMeta.read_only_fields

