from rest_framework import serializers

from workflow.models import Workflow, Patient
from django.forms.models import model_to_dict

from common.base_serializers import ImmutableSerializerMeta, CurrentSerializerMeta, BaseSaveSerializer

import stringcase


class PatientSerializer(BaseSaveSerializer, serializers.ModelSerializer):

    class Meta:
        model = Patient

        fields = ImmutableSerializerMeta.base_fields
        read_only_fields=ImmutableSerializerMeta.read_only_fields


class GenericData(serializers.RelatedField):
    def to_representation(self, value):
        # TODO: handle this correctly for any serializer
        data = PatientSerializer(value).data
        d = {stringcase.snakecase(value.__class__.__name__): data}
        return d


class WorkflowSerializer(BaseSaveSerializer, serializers.ModelSerializer):

    related_data=GenericData(many=False, read_only=True)

    class Meta:
        # TODO handle this properly
        model=Workflow
        extra_kwargs={
            'related_data': {'read_only': True}
        }

        fields=ImmutableSerializerMeta.base_fields + ['workflow_type', 'related_data']

        read_only_fields=ImmutableSerializerMeta.read_only_fields
