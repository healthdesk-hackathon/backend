from django.test import TestCase

# Create your tests here.
from workflow.models import Workflow


class WorkflowTest(TestCase):

    def test_data_migration_added_a_workflow_model(self):
        self.assertEqual(Workflow.objects.count(), 1)
