from rest_framework import serializers

from patient.models import Patient, PersonalData, NextOfKinContact, Phone


class PatientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Patient
        fields = [
            'id',

        ]


class PersonalDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonalData
        fields = [
            'id',
            'first_name',
            'last_name',
            'gender',
            'date_of_birth',

        ]


class PhoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Phone
        fields = [
            'id',
            'phone_number',
            'phone_type',
        ]


class NextOfKinContactSerializer(serializers.ModelSerializer):

    class Meta:
        model = NextOfKinContact
        extra_kwargs = {
            'created': {'read_only': True}
        }
        fields = [


            'first_name',
            'last_name',
            'title',
            'relationship',
            'other_relationship',
            'phone_number',
            'notes',
        ]

