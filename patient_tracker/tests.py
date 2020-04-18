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

    def test_admit_patient(self):

        patient = Patient.objects.create(identifier='12346', current_user=self.test_user)
        admission = Admission.objects.create(patient=patient, current_user=self.test_user)
        icu = BedType.objects.get(name='Intensive Care Unit')

        assigned_bed = admission.assign_bed(icu)
        self.assertTrue(assigned_bed)
        self.assertEqual(icu.number_assigned, 1)
        self.assertEqual(icu.number_available, 1)
        self.assertEqual(icu.number_out_of_service, 0)

        admission2 = Admission.objects.create(patient=patient, current_user=self.test_user)
        admission2.assign_bed(icu)
        self.assertEqual(icu.number_assigned, 2)
        self.assertEqual(icu.number_available, 0)
        self.assertEqual(icu.number_out_of_service, 0)

        admission3 = Admission.objects.create(patient=patient, current_user=self.test_user)

        self.assertRaises(Bed.DoesNotExist, lambda: admission3.assign_bed(icu))
        self.assertEqual(icu.number_assigned, 2)
        self.assertEqual(icu.number_available, 0)

    def test_change_bed(self):
        patient = Patient.objects.create(identifier='12347', current_user=self.test_user)
        admission = Admission.objects.create(patient=patient, current_user=self.test_user)
        icu = BedType.objects.get(name='Intensive Care Unit')
        inter = BedType.objects.get(name='Intermediate Care')

        admission.assign_bed(bed_type=icu)
        self.assertEqual(icu.number_assigned, 1)
        self.assertEqual(icu.number_available, 1)
        self.assertEqual(icu.number_out_of_service, 0)

        self.assertEqual(inter.number_assigned, 0)
        self.assertEqual(inter.number_available, 3)
        self.assertEqual(inter.number_out_of_service, 0)

        # Assign a new bed to the admission
        admission.assign_bed(bed_type=inter)
        # The number of available intermediate beds should be reduced by one as one is assigned
        self.assertEqual(inter.number_assigned, 1)
        self.assertEqual(inter.number_available, 2)
        self.assertEqual(inter.number_out_of_service, 0)
        # The number of ICU beds available remains at one, none are now assigned but one is out of service
        self.assertEqual(icu.number_assigned, 0)
        self.assertEqual(icu.number_available, 1)
        self.assertEqual(icu.number_out_of_service, 1)

    def test_discharge(self):

        patient = Patient.objects.create(identifier='12346', current_user=self.test_user)
        admission = Admission.objects.create(patient=patient, current_user=self.test_user)
        icu = BedType.objects.get(name='Intensive Care Unit')
        # inter = BedType.objects.get(name='Intermediate Care')

        admission.assign_bed(bed_type=icu)
        self.assertEqual(icu.number_assigned, 1)
        self.assertEqual(icu.number_available, 1)
        self.assertEqual(icu.number_out_of_service, 0)

        admission.discharge()
        # We leave the bed, taking it out of service
        self.assertTrue(admission.is_discharged)
        self.assertEqual(icu.number_assigned, 0)
        self.assertEqual(icu.number_available, 1)
        self.assertEqual(icu.number_out_of_service, 1)
