from django.test import TestCase

# Create your tests here.
from dummy.models import Dummy


class DummyTest(TestCase):

    def test_data_migration_added_a_dummy_model(self):
        self.assertEqual(Dummy.objects.count(), 1)
