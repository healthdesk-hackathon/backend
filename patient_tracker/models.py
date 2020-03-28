import hashlib
import uuid

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from submission.models import Submission

class Admission(models.Model):
    """
    Represents the admission into the hospital system, when the admins / triage have
    performed the initial steps for getting the patient into the system.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    local_barcode = models.CharField(max_length=150, unique=True)
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE, related_name='admissions')
