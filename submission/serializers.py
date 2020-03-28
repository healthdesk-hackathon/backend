from rest_framework import serializers

from submission.models import Patient, Submission, PersonalData, Phone, OverallWellbeing, CommonSymptoms, \
    GradedSymptoms, RelatedConditions


class OverallWellbeingSerializer(serializers.ModelSerializer):

    class Meta:
        model = OverallWellbeing
        fields = [
            'id',
            'overall_value',
            'submission'
        ]


class CommonSymptomsSerializer(serializers.ModelSerializer):

    class Meta:
        model = CommonSymptoms
        fields = [
            'id',

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
            'submission'
        ]


class GradedSymptomsSerializer(serializers.ModelSerializer):
    """
    Symptoms that a patient grades on a scale of 0 to 10
    """

    class Meta:
        model = GradedSymptoms
        fields = [
            'id',
            'submission',
            'difficulty_breathing',
            'anxious'
        ]


class RelatedConditionsSerializer(serializers.ModelSerializer):

    class Meta:
        model = RelatedConditions
        fields = [
            'id',
            'submission',

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
    persons = PersonalDataSerializer(many=True, read_only=True)
    common_symptoms = CommonSymptomsSerializer(read_only=True)
    graded_symptoms = GradedSymptomsSerializer(read_only=True)
    related_conditions = RelatedConditionsSerializer(read_only=True)

    class Meta:
        model = Submission
        fields = [
            'id',
            'identifier',
            'id_type',
            'phones',
            'persons',
            'common_symptoms',
            'graded_symptoms',
            'related_conditions'
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
