import sys
import uuid

from model_utils.models import TimeStampedModel, SoftDeletableModel
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from simple_history.models import HistoricalRecords

TEST = 'test' in sys.argv


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

    def __init__(self, *args, **kwargs):
        if not hasattr(self, '_current_user'):
            self._current_user = None
        super().__init__(*args, **kwargs)

    class Meta:
        abstract = True

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT,
                                null=False, related_name='%(class)s_creator')

    @property
    def current_user(self):
        return self._current_user

    @current_user.setter
    def current_user(self, value):
        self._current_user = value

    def prevent_update(self):
        """prevent a record from being saved if it has a pk"""
        if self.pk:
            raise ValidationError('record must not be updated')

    def save(self, **kwargs):
        if not self.creator_id:
            # Only set added_by during the first save.
            self.creator = self.current_user
        super().save(**kwargs)


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

    Subclasses also gain a history, which generates a new table tracking changes made to the primary model.
    Every time a create, update, or delete occurs on the primary instance, a new record is created in the history.

    View (https://django-simple-history.readthedocs.io/en/latest/) for docs for django-simple-history
    """

    def __init__(self, *args, **kwargs):
        if not hasattr(self, '_current_user'):
            self._current_user = None
        super().__init__(*args, **kwargs)

    class Meta:
        abstract = True

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT,
                                null=False, related_name='%(class)s_creator')
    modifier = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT,
                                 null=True, related_name='%(class)s_modifier')
    history = HistoricalRecords(inherit=True)

    @property
    def current_user(self):
        return self._current_user

    @current_user.setter
    def current_user(self, value):
        self._current_user = value

    def save(self, **kwargs):
        if not self.creator_id:
            # Only set added_by during the first save.
            self.creator = self.current_user
        else:
            # Set the modifier on every save
            self.modifier = self.current_user
        super().save(**kwargs)
