from django.shortcuts import render
from rest_framework import viewsets, permissions

from dummy.models import Dummy
from dummy.serializers import DummySerializer


class DummyViewSet(viewsets.ModelViewSet):
    queryset = Dummy.objects.all()
    serializer_class = DummySerializer

    permission_classes = [permissions.AllowAny]
