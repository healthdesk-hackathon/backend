from django.test import TestCase

# Create your tests here.
from dummy.models import Dashboard


class DashboardTest(TestCase):

    def test_data_migration_added_a_dashboard_model(self):
        self.assertEqual(Dashboard.objects.count(), 1)
