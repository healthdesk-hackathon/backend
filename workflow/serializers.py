import sys
from rest_framework import serializers

from workflow.models import Workflow, Patient, Admission
from patient.models import PersonalData
from django.contrib.contenttypes.models import ContentType

from common.base_serializers import ImmutableSerializerMeta, CurrentSerializerMeta, BaseSaveSerializer, SerializerMixin
import stringcase

from patient.serializers import PersonalDataSerializer, PatientIdentifierSerializer, PhoneSerializer, NextOfKinContactSerializer


class PatientSerializer(BaseSaveSerializer, serializers.ModelSerializer):
    personal_data = PersonalDataSerializer()
    patient_identifiers = PatientIdentifierSerializer(many=True)
    phones = PhoneSerializer(many=True)
    next_of_kin_contacts = NextOfKinContactSerializer(many=True)

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
        depth=2


class AdmissionSerializer(BaseSaveSerializer, serializers.ModelSerializer):
    patient_id=serializers.PrimaryKeyRelatedField(source='patient', write_only=True, queryset=Patient.objects.all())
    patient = PatientSerializer()

    class Meta:
        model = Admission
        extra_kwargs = {
            'patient': {'read_only': True},
            'patient_id': {'read_only': True},

        }

        fields = CurrentSerializerMeta.base_fields + ['patient', 'patient_id']
        read_only_fields=CurrentSerializerMeta.read_only_fields
        depth=3


class GenericData(SerializerMixin, serializers.RelatedField):

    def to_internal_value(self, data):
        d = None
        if data:
            cname = data.get('rel_type')
            cid = data.get('rel_id')
            if cid and cname:
                c = self.str_to_class(cname)
                d = c.objects.get(id=cid)
        return d

    def to_representation(self, inst):

        # A serializer class based on the name of the model
        cname = inst.__class__.__name__ + "Serializer"

        # Get this module and use it to find the serializer class
        thismodule = sys.modules[__name__]
        serializer_class = getattr(thismodule, cname)

        # Instantiate the serializer with the instance and get the resulting serializable data
        serializable_data = serializer_class(inst).data

        # Formulate the final dict to return, using the underscored model name as a key
        dict_data = {stringcase.snakecase(inst.__class__.__name__): serializable_data}

        return dict_data


class WorkflowSerializer(BaseSaveSerializer, serializers.ModelSerializer):

    related_data = GenericData(many=False, queryset=ContentType.objects.all())

    class Meta:
        model = Workflow

        fields=ImmutableSerializerMeta.base_fields + ['workflow_type',
                                                      'related_data', 'rel_id', 'rel_type']

        read_only_fields=ImmutableSerializerMeta.read_only_fields

    def create(self, validated_data):
        rel = validated_data["related_data"]
        if rel:
            validated_data["rel_type"] = ContentType.objects.get_for_model(rel.__class__)
            validated_data["rel_id"] = rel.id

        del validated_data["related_data"]

        return super().create(validated_data)
