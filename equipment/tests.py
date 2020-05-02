from django.test import TestCase, RequestFactory

from patient.models import Patient
from patient_tracker.models import Admission
from equipment.models import BedType, Bed
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from common.base_tests import TestUser


class PatientTrackerTestCase(TestCase, TestUser):

    def setUp(self):

        BedType.objects.create(name="Intensive Care Unit", severity_match='RED', total=2, current_user=self.test_user)
        BedType.objects.create(name="Intermediate Care", severity_match='YELLOW', total=3, current_user=self.test_user)
        return

    def test_autocreate_beds(self):
        self.assertEqual(Bed.objects.filter(bed_type__name="Intensive Care Unit").count(), 2)
        self.assertEqual(Bed.objects.filter(bed_type__name="Intermediate Care").count(), 3)
        self.assertEqual(Bed.objects.available().count(), 5)
