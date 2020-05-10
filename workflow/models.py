from django.db import models
from common.base_models import ImmutableBaseModel, CurrentBaseModel
from patient.models import Patient


# Create your models here.


class Workflow(ImmutableBaseModel):

    workflow_type = models.CharField(max_length=30)

    @property
    def related_data(self):
        """faking how this might work in practice
        """

        if self.workflow_type == 'register patient':
            data = Patient()
            data.current_user = self.current_user
            data.save()
            return data
