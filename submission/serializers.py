from rest_framework import serializers

from submission.models import Patient, Submission, Admission, PersonalData, Phone


class PersonalDataSerializer(serializers.ModelSerializer):

    class Meta:
        model = PersonalData
        fields = [
            'id',
            'first_name',
            'last_name',
            'gender',
            'date_of_birth',
            'submission'
        ]


class AdmissionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Admission
        fields = [
            'id',
            'local_barcode',
            'submission'
        ]


class PhoneSerializer(serializers.ModelSerializer):

    class Meta:
        model = Phone
        fields = [
            'id',
            'phone_number',
            'phone_type',
            'rank',
            'verified',
            'disabled',
            'submission'
        ]


class SubmissionSerializer(serializers.ModelSerializer):

    phones = PhoneSerializer(many=True, read_only=True)
    admissions = AdmissionSerializer(many=True, read_only=True)
    persons = PersonalDataSerializer(many=True, read_only=True)

    class Meta:
        model = Submission
        fields = [
            'id',
            'identifier',
            'id_type',
            'phones',
            'admissions',
            'persons'
        ]


class PatientSerializer(serializers.ModelSerializer):

    submissions = SubmissionSerializer(many=True, read_only=True)

    class Meta:
        model = Patient
        fields = [
            'id',
            'anon_patient_id',
            'submissions'
        ]
