from django.contrib import admin
import hashlib
import uuid

from django.db import models

class MedicalCenter(models.Model):
    """
    Available medical centers, from which a patient can choose.

    This is as limited set of attributes, to reflect what is needed for a simple, 
    GPS located submission.

    Addtional address information could be added in the future if necessary.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    name = models.CharField(max_length=50, blank=False)
    latitude = models.FloatField(null=False)
    longitude = models.FloatField(null=False)
