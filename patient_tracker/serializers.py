from rest_framework import serializers

from submission.models import Submission
from patient_tracker.models import Admission


class AdmissionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Admission
        fields = [
            'id',
            'local_barcode',
            'submission'
        ]


