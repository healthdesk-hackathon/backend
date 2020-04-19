from rest_framework import serializers


class LabelledValueSerializer(serializers.Serializer):
    label = serializers.CharField()
    value = serializers.FloatField()


class AdmissionCountSerializer(serializers.Serializer):

    date = serializers.DateField()
    count = LabelledValueSerializer(many=True)


class DashboardSerializer(serializers.Serializer):
    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    bed_availability = LabelledValueSerializer(many=True, required=False)
    assignments = LabelledValueSerializer(many=True, )
    global_availability = serializers.FloatField(required=False)
    total_discharges = serializers.IntegerField(required=False)
    average_duration = serializers.DurationField(required=False, allow_null=True)
    admissions_per_day = AdmissionCountSerializer(many=True, required=False)

    class Meta:
        fields = [
            'bed_availability',
            'global_availability',
            'total_discharges',
            'assignments',
            'average_duration'
        ]

