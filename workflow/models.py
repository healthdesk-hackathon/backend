from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

import json

from common.base_models import ImmutableBaseModel, CurrentBaseModel
from patient.models import Patient
from patient_tracker.models import Admission
import stringcase


# Create your models here.


class Workflow(ImmutableBaseModel):

    workflow_type = models.CharField(max_length=30)

    rel_type = models.ForeignKey(ContentType, null=True, on_delete=models.CASCADE)
    rel_id = models.UUIDField(null=True)
    related_item = GenericForeignKey('rel_type', 'rel_id')

    @property
    def related_data(self):
        return self.related_item

    def save(self, **kwargs):
        """On saving a workflow, related data needs to be generated

        Make a call to the method represented by the workflow_type. This will
        generate a related model and any additional input data
        """

        workflow_method = getattr(self, stringcase.snakecase(self.workflow_type))
        data = workflow_method()
        self.related_item = data

        return super().save(**kwargs)

    def register_patient(self):
        data = Patient()
        data.current_user = self.current_user
        data.save()
        return data

    def admit_patient(self):
        data = Admission(patient_id=self.related_data.id, admitted=False)
        data.current_user = self.current_user
        data.save()
        return data

    def triage_submission(self):
        patient_data = Patient()
        patient_data.current_user = self.current_user
        patient_data.save()
        data = Admission(patient_id=patient_data.id, admitted=False)
        data.current_user = self.current_user
        data.save()
        return data
