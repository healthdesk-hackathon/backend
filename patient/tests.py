from django.test import TestCase

from patient_tracker.models import Admission, HealthSnapshot
from equipment.models import BedType, Bed
from patient.models import Patient
from django.core.exceptions import ValidationError, ObjectDoesNotExist

from common.base_tests import TestUser


class AutoAssignBedTestCase(TestCase, TestUser):
    def setUp(self):

        BedType.objects.create(name="Intensive Care Unit", severity_match="RED", total=2, current_user=self.test_user)
        BedType.objects.create(name="Intermediate Care", severity_match="YELLOW", total=3, current_user=self.test_user)
        BedType.objects.create(name="Recovery", severity_match="GREEN", total=3, current_user=self.test_user)
        return

    def test_auto_assign_bed_on_admission(self):

        patient = Patient(current_user=self.test_user)
        patient.save()

        admission = Admission.objects.create(patient=patient, current_user=self.test_user)

        init_hs = HealthSnapshot(
            admission=admission,
            blood_pressure_systolic=3,
            blood_pressure_diastolic=4,
            heart_rate=5,
            breathing_rate=6,
            temperature=7,
            oxygen_saturation=8,
            gcs_eye=1,
            gcs_verbal=12,
            gcs_motor=3,
            observations="Text notes",
            severity=HealthSnapshot.SeverityChoices.YELLOW,
            current_user=self.test_user
        )

        init_hs.save()

        admission = patient.current_admission
        self.assertTrue(admission)

        bed = admission.current_bed

        # TODO: This will currently fail, as the workflow manager will need to perform the
        # assignment of a bed at the end of the admission process
        self.assertTrue(bed)

        self.assertEqual(bed.bed_type.name, "Intermediate Care")

    def test_no_auto_assign_bed_if_no_match(self):

        patient = Patient(current_user=self.test_user)
        patient.save()

        admission = Admission.objects.create(patient=patient, current_user=self.test_user)

        init_hs = HealthSnapshot(
            admission=admission,
            blood_pressure_systolic=3,
            blood_pressure_diastolic=4,
            heart_rate=5,
            breathing_rate=6,
            temperature=7,
            oxygen_saturation=8,
            gcs_eye=1,
            gcs_verbal=12,
            gcs_motor=3,
            observations="Text notes",
            severity='BLACK',
            current_user=self.test_user
        )

        init_hs.save()

        admission = patient.current_admission
        self.assertTrue(admission)

        bed = admission.current_bed
        self.assertFalse(bed)



