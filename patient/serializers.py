from rest_framework import serializers

from patient.models import Patient, PatientIdentifier, PersonalData, NextOfKinContact, Phone
from common.base_serializers import ImmutableSerializerMeta, CurrentSerializerMeta, BaseSaveSerializer


class PatientSerializer(BaseSaveSerializer, serializers.ModelSerializer):

    class Meta:
        model = Patient

        extra_kwargs={
            'current_admission_id': {'read_only': True}
        }

        fields = ImmutableSerializerMeta.base_fields + [
            'current_admission_id'
        ]
        read_only_fields=ImmutableSerializerMeta.read_only_fields


class PatientIdentifierSerializer(BaseSaveSerializer, serializers.ModelSerializer):

    class Meta:
        model=PatientIdentifier
        fields=ImmutableSerializerMeta.base_fields + [
            'identifier',
            'id_type'
        ]
        read_only_fields=ImmutableSerializerMeta.read_only_fields


class PersonalDataSerializer(BaseSaveSerializer, serializers.ModelSerializer):
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
    class Meta:
        model=Phone
        fields=CurrentSerializerMeta.base_fields + [
            'patient_id',
            'phone_number',
            'phone_type',
        ]
        read_only_fields=CurrentSerializerMeta.read_only_fields


class NextOfKinContactSerializer(BaseSaveSerializer, serializers.ModelSerializer):

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

