from rest_framework import serializers

from equipment.models import Bed, BedType
from patient_tracker.serializers import AdmissionSerializer
from common.base_serializers import ImmutableSerializerMeta, CurrentSerializerMeta


class BedSerializer(serializers.ModelSerializer):

    current_admission = AdmissionSerializer(read_only=True)

    class Meta:
        model = Bed
        fields = CurrentSerializerMeta.base_fields + [
            'bed_type',
            'assignments',
            'reason',
            'state',
            'current_admission',
        ]


class BedTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = BedType
        extra_kwargs = {
            'number_out_of_service': {'read_only': True},
            'number_assigned': {'read_only': True},
            'number_available': {'read_only': True},
            'number_waiting': {'read_only': True},
            'is_available': {'read_only': True},
        }
        fields = CurrentSerializerMeta.base_fields + [
            'name',
            'total',

            'number_out_of_service',
            'number_assigned',
            'number_available',
            'number_waiting',
            'is_available',
        ]

