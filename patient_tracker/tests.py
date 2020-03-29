from django.test import TestCase

from patient_tracker.models import Admission, BedType, Bed
from django.core.exceptions import ValidationError, ObjectDoesNotExist

class PatientTrackerTestCase(TestCase):
    def setUp(self):
        BedType.objects.create(name="Intensive Care Unit", total=2)
        BedType.objects.create(name="Intermediate Care", total=3)
        return

    def test_autocreate_beds(self):
        self.assertEqual(Bed.objects.filter(bed_type__name="Intensive Care Unit").count(), 2)
        self.assertEqual(Bed.objects.filter(bed_type__name="Intermediate Care").count(), 3)
        self.assertEqual(Bed.objects.available().count(), 5)

    def test_admit_patient(self):

        admission = Admission.objects.create()
        icu = BedType.objects.get(name='Intensive Care Unit')

        assigned_bed = admission.assign_bed(icu)
        self.assertTrue(assigned_bed)
        self.assertEqual(icu.number_assigned, 1)
        self.assertEqual(icu.number_available, 1)
        self.assertEqual(icu.number_out_of_service, 0)

        admission2 = Admission.objects.create()
        admission2.assign_bed(icu)
        self.assertEqual(icu.number_assigned, 2)
        self.assertEqual(icu.number_available, 0)
        self.assertEqual(icu.number_out_of_service, 0)

        admission3 = Admission.objects.create()

        self.assertRaises(Bed.DoesNotExist, lambda: admission3.assign_bed(icu))
        self.assertEqual(icu.number_assigned, 2)
        self.assertEqual(icu.number_available, 0)

    def test_change_bed(self):
        admission = Admission.objects.create()
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

        admission = Admission.objects.create()
        icu = BedType.objects.get(name='Intensive Care Unit')
        inter = BedType.objects.get(name='Intermediate Care')

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
