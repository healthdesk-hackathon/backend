from django.test import TestCase

from patient_tracker.models import Patient, Admission, BedType, Bed
from submission.models import Submission, InitialHealthSnapshot
from django.core.exceptions import ValidationError, ObjectDoesNotExist


class AutoAssignBedTestCase(TestCase):
    def setUp(self):
        BedType.objects.create(name="Intensive Care Unit", severity_match="RED", total=2)
        BedType.objects.create(name="Intermediate Care", severity_match="YELLOW", total=3)
        BedType.objects.create(name="Recovery", severity_match="GREEN", total=3)
        return

    def test_auto_assign_bed_on_admission(self):

        patient = Patient(anon_patient_id='12345')
        patient.save()
        submission = Submission(patient=patient)
        submission.save()

        init_hs = InitialHealthSnapshot(submission=submission,
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
                                        severity=InitialHealthSnapshot.SeverityChoices.YELLOW,
                                        )

        init_hs.save()

        admission = patient.current_admission
        self.assertTrue(admission)

        bed = admission.current_bed
        self.assertTrue(bed)

        self.assertEqual(bed.bed_type.name, "Intermediate Care")

    def test_no_auto_assign_bed_if_no_match(self):

        patient = Patient(anon_patient_id='12346')
        patient.save()
        submission = Submission(patient=patient)
        submission.save()

        init_hs = InitialHealthSnapshot(submission=submission,
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
                                        )

        init_hs.save()

        admission = patient.current_admission
        self.assertTrue(admission)

        bed = admission.current_bed
        self.assertFalse(bed)



