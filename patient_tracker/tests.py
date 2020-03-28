from django.test import TestCase

from patient_tracker.models import Admission, BedType, AssignedBed, OutOfServiceBed

class PatientTrackerTestCase(TestCase):
    def setUp(self):
        BedType.objects.create(name="Intensive Care Unit", total=10)
        BedType.objects.create(name="Intermediate Care", total=10)
        return

    def test_admit_patient(self):
        
        admission = Admission.objects.create()
        self.assertTrue(hasattr(admission, 'assigned_beds'))

        icu = BedType.objects.filter(name='Intensive Care Unit').first()
        
        assigned_bed = AssignedBed(admission = admission, bed_type=icu)
        assigned_bed.save()
        self.assertTrue(assigned_bed)
        self.assertEqual(icu.number_assigned(), 1)
        self.assertEqual(icu.number_available(), 9)
