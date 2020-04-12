import hashlib
import uuid

from model_utils.models import TimeStampedModel, SoftDeletableModel
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models


class ImmutableBaseModel(SoftDeletableModel, TimeStampedModel):
    """Used as a base class for models that are immutable and additive over time.

    A subclass is expected to always provide a user model for creation. If subclasses are
    to be saved outside of an authenticated user session, a common 'automated user' should be applied, 
    allowing audit to confirm that an automated task generated the record.

    As a default, it provides attributes:

      id -- UUID
      creator -- User that created the record
      created -- Timestamp the model was created
      is_removed -- True if the instance is to be considered deleted and ignored in queries
    """

    class Meta:
        abstract = True

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT,
                                null=False, related_name='%(class)s_creator')

    def prevent_update(self):
        """prevent a record from being saved if it has a pk"""
        if self.pk:
            raise ValidationError('record must not be updated')

    def save_model(self, request, obj, form, change):
        self.prevent_update()

        if not obj.pk:
            # Only set added_by during the first save.
            obj.created = request.user
        super().save_model(request, obj, form, change)


class CurrentBaseModel(TimeStampedModel):
    """Used as a base class for models that hold are updatable to hold current values.

    A subclass is expected to always provide a user model for creation or modification. If subclasses are
    to be saved outside of an authenticated user session, a common 'automated user' should be applied, 
    allowing audit to confirm that an automated task generated or modified the record.

    As a default, it provides attributes:

      id -- UUID
      creator -- User that created the record
      created -- Timestamp the model was created
      modifier -- User that modified the record
      modified -- Timestamp the model was modified
    """

    class Meta:
        abstract = True

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT,
                                null=False, related_name='%(class)s_creator')
    modifier = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT,
                                 null=True, related_name='%(class)s_modifier')

    def save_model(self, request, obj, form, change):
        if obj.pk:
            # Set the modifier on every save
            obj.modifier = request.user
        else:
            # Only set added_by during the first save.
            obj.created = request.user
        super().save_model(request, obj, form, change)
