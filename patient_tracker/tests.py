from django.test import TestCase

from patient_tracker.models import Admission, BedType, AssignedBed, OutOfServiceBed
from django.core.exceptions import ValidationError, ObjectDoesNotExist

class PatientTrackerTestCase(TestCase):
    def setUp(self):
        BedType.objects.create(name="Intensive Care Unit", total=2)
        BedType.objects.create(name="Intermediate Care", total=3)
        return

    def test_admit_patient(self):
        
        admission = Admission.objects.create()
        icu = BedType.objects.filter(name='Intensive Care Unit').first()
        
        assigned_bed = AssignedBed(admission = admission, bed_type=icu)
        assigned_bed.save()
        self.assertTrue(assigned_bed)
        self.assertEqual(icu.number_assigned(), 1)
        self.assertEqual(icu.number_available(), 1)
        self.assertEqual(icu.number_out_of_service(), 0)

        admission2 = Admission.objects.create()
        assigned_bed = AssignedBed(admission = admission2, bed_type=icu)
        assigned_bed.save()
        self.assertEqual(icu.number_assigned(), 2)
        self.assertEqual(icu.number_available(), 0)
        self.assertEqual(icu.number_out_of_service(), 0)

        admission3 = Admission.objects.create()
        assigned_bed = AssignedBed(admission = admission3, bed_type=icu)
        
        self.assertRaises(ObjectDoesNotExist, assigned_bed.save)
        self.assertEqual(icu.number_assigned(), 2)
        self.assertEqual(icu.number_available(), 0)
        
    def test_change_bed(self):
        admission = Admission.objects.create()
        icu = BedType.objects.filter(name='Intensive Care Unit').first()
        inter = BedType.objects.filter(name='Intermediate Care').first()
        
        assigned_bed = admission.assign_bed(bed_type=icu)
        assigned_bed.save()
        self.assertEqual(icu.number_assigned(), 1)
        self.assertEqual(icu.number_available(), 1)
        self.assertEqual(icu.number_out_of_service(), 0)

        self.assertEqual(inter.number_assigned(), 0)
        self.assertEqual(inter.number_available(), 3)
        self.assertEqual(inter.number_out_of_service(), 0)


        # Assign a new bed to the admission
        new_bed = admission.assign_bed(bed_type=inter)
        new_bed.save()
        # The number of available intermediate beds should be reduced by one as one is assigned
        self.assertEqual(inter.number_assigned(), 1)
        self.assertEqual(inter.number_available(), 2)
        self.assertEqual(inter.number_out_of_service(), 0)
        # The number of ICU beds available remains at one, none are now assigned but one is out of service
        self.assertEqual(icu.number_assigned(), 0)
        self.assertEqual(icu.number_available(), 1)
        self.assertEqual(icu.number_out_of_service(), 1)
