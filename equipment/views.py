from rest_framework import viewsets, permissions, mixins
from rest_framework.viewsets import ModelViewSet
from equipment.models import Bed, BedType
from equipment.serializers import BedSerializer, BedTypeSerializer

equipment_permissions = [permissions.DjangoModelPermissions]


class BedViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    queryset = Bed.objects.all()
    serializer_class = BedSerializer

    permission_classes = equipment_permissions


class BedTypeViewSet(ModelViewSet):
    queryset = BedType.objects.all()
    serializer_class = BedTypeSerializer

    permission_classes = equipment_permissions

