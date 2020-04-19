from rest_framework import serializers

from patient.models import Patient, PatientIdentifier, PersonalData, NextOfKinContact, Phone
from common.base_serializers import ImmutableSerializerMeta, CurrentSerializerMeta


class PatientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Patient
        fields = ImmutableSerializerMeta.base_fields


class PatientIdentifierSerializer(serializers.ModelSerializer):

    class Meta:
        model = PatientIdentifier
        fields = ImmutableSerializerMeta.base_fields + [
            'identifier',
            'id_type'
        ]


class PersonalDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonalData
        fields = CurrentSerializerMeta.base_fields + [
            'patient_id',
            'first_name',
            'last_name',
            'gender',
            'date_of_birth',
        ]


class PhoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Phone
        fields = CurrentSerializerMeta.base_fields + [
            'patient_id',
            'phone_number',
            'phone_type',
        ]


class NextOfKinContactSerializer(serializers.ModelSerializer):

    class Meta:
        model = NextOfKinContact

        fields = CurrentSerializerMeta.base_fields + [
            'patient_id',
            'first_name',
            'last_name',
            'title',
            'relationship',
            'other_relationship',
            'phone_number',
            'notes',
        ]

