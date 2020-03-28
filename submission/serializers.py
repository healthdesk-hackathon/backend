from rest_framework import serializers

from submission.models import Master, Submission, Admission, Person, Phone


class PersonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Person
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
    persons = PersonSerializer(many=True, read_only=True)

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


class MasterSerializer(serializers.ModelSerializer):

    submissions = SubmissionSerializer(many=True, read_only=True)

    class Meta:
        model = Master
        fields = [
            'id',
            'anon_patient_id',
            'submissions'
        ]
