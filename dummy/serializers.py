from rest_framework import serializers

from dummy.models import Dummy


class DummySerializer(BaseSaveSerializer, serializers.ModelSerializer):
    class Meta:
        model=Dummy
        fields=['id', 'greeting', 'target']
