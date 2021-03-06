# Generated by Django 3.0.6 on 2020-05-23 19:39

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields
import simple_history.models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('patient', '0006_auto_20200422_2010'),
        ('equipment', '0002_historicalbed_historicalbedtype'),
    ]

    operations = [
        migrations.CreateModel(
            name='Admission',
            fields=[
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('local_barcode', models.CharField(max_length=13, null=True, unique=True)),
                ('local_barcode_image', models.ImageField(null=True, upload_to='')),
                ('admitted_at', models.DateTimeField(default=None, null=True)),
                ('admitted', models.BooleanField(default=True)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='admission_creator', to=settings.AUTH_USER_MODEL)),
                ('modifier', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='admission_modifier', to=settings.AUTH_USER_MODEL)),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='admissions', to='patient.Patient')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='HealthSnapshot',
            fields=[
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('is_removed', models.BooleanField(default=False)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('main_complain', models.CharField(blank=True, default='', max_length=250, null=True)),
                ('blood_pressure_systolic', models.PositiveIntegerField(blank=True, null=True)),
                ('blood_pressure_diastolic', models.PositiveIntegerField(blank=True, null=True)),
                ('heart_rate', models.PositiveIntegerField(blank=True, null=True)),
                ('breathing_rate', models.PositiveIntegerField(blank=True, null=True)),
                ('temperature', models.FloatField(blank=True, null=True)),
                ('oxygen_saturation', models.PositiveIntegerField(blank=True, null=True)),
                ('gcs_eye', models.PositiveSmallIntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(4)], verbose_name='GCS eye')),
                ('gcs_verbal', models.PositiveSmallIntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)], verbose_name='GCS verbal')),
                ('gcs_motor', models.PositiveSmallIntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(6)], verbose_name='GCS motor')),
                ('observations', models.TextField(blank=True, null=True)),
                ('severity', models.CharField(choices=[('RED', 'Red'), ('YELLOW', 'Yellow'), ('GREEN', 'Green'), ('WHITE', 'White')], max_length=6)),
                ('admission', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='health_snapshots', to='patient_tracker.Admission')),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='healthsnapshot_creator', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created'],
            },
        ),
        migrations.CreateModel(
            name='RelatedConditions',
            fields=[
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('is_removed', models.BooleanField(default=False)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('heart_condition', models.BooleanField(default=False)),
                ('high_blood_pressure', models.BooleanField(default=False)),
                ('asthma', models.BooleanField(default=False)),
                ('chronic_lung_problems', models.BooleanField(default=False)),
                ('mild_diabetes', models.BooleanField(default=False)),
                ('chronic_diabetes', models.BooleanField(default=False)),
                ('current_chemo', models.BooleanField(default=False)),
                ('past_chemo', models.BooleanField(default=False)),
                ('take_immunosuppressants', models.BooleanField(default=False)),
                ('pregnant', models.BooleanField(default=False)),
                ('smoke', models.BooleanField(default=False)),
                ('admission', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='related_conditions', to='patient_tracker.Admission')),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='relatedconditions_creator', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='OverallWellbeing',
            fields=[
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('is_removed', models.BooleanField(default=False)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('overall_value', models.IntegerField(validators=[django.core.validators.MaxValueValidator(10), django.core.validators.MinValueValidator(0)])),
                ('admission', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='overall_wellbeing', to='patient_tracker.Admission')),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='overallwellbeing_creator', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='HistoricalAdmission',
            fields=[
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('id', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False)),
                ('local_barcode', models.CharField(db_index=True, max_length=13, null=True)),
                ('local_barcode_image', models.TextField(max_length=100, null=True)),
                ('admitted_at', models.DateTimeField(default=None, null=True)),
                ('admitted', models.BooleanField(default=True)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('creator', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('modifier', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('patient', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='patient.Patient')),
            ],
            options={
                'verbose_name': 'historical admission',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HealthSnapshotFile',
            fields=[
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('is_removed', models.BooleanField(default=False)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('file', models.ImageField(upload_to='health_snapshot_file')),
                ('notes', models.TextField()),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='healthsnapshotfile_creator', to=settings.AUTH_USER_MODEL)),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='health_snapshot_files', to='patient_tracker.HealthSnapshot')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='GradedSymptoms',
            fields=[
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('is_removed', models.BooleanField(default=False)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('difficulty_breathing', models.IntegerField(validators=[django.core.validators.MaxValueValidator(10), django.core.validators.MinValueValidator(0)])),
                ('anxious', models.IntegerField(validators=[django.core.validators.MaxValueValidator(10), django.core.validators.MinValueValidator(0)])),
                ('admission', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='graded_symptoms', to='patient_tracker.Admission')),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='gradedsymptoms_creator', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Discharge',
            fields=[
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('is_removed', models.BooleanField(default=False)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('discharged_at', models.DateTimeField(auto_now_add=True)),
                ('notes', models.TextField(blank=True, null=True)),
                ('admission', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='discharge_events', to='patient_tracker.Admission')),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='discharge_creator', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Deceased',
            fields=[
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('is_removed', models.BooleanField(default=False)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('registered_at', models.DateTimeField(null=True)),
                ('cause', models.CharField(max_length=100)),
                ('notes', models.TextField(blank=True, null=True)),
                ('notified_next_of_kin', models.BooleanField(default=False)),
                ('admission', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='deceased_event', to='patient_tracker.Admission')),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='deceased_creator', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CommonSymptoms',
            fields=[
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('is_removed', models.BooleanField(default=False)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('chills', models.BooleanField(default=False)),
                ('achy_joints_muscles', models.BooleanField(default=False)),
                ('lost_taste_smell', models.BooleanField(default=False)),
                ('congestion', models.BooleanField(default=False)),
                ('stomach_disturbance', models.BooleanField(default=False)),
                ('tiredness', models.BooleanField(default=False)),
                ('headache', models.BooleanField(default=False)),
                ('dry_cough', models.BooleanField(default=False)),
                ('cough_with_sputum', models.BooleanField(default=False)),
                ('nauseous', models.BooleanField(default=False)),
                ('short_of_breath', models.BooleanField(default=False)),
                ('sore_throat', models.BooleanField(default=False)),
                ('fever', models.BooleanField(default=False)),
                ('runny_nose', models.BooleanField(default=False)),
                ('admission', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='common_symptoms', to='patient_tracker.Admission')),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='commonsymptoms_creator', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='BedAssignment',
            fields=[
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('is_removed', models.BooleanField(default=False)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('assigned_at', models.DateTimeField(auto_now_add=True)),
                ('unassigned_at', models.DateTimeField(blank=True, default=None, null=True)),
                ('admission', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assignments', to='patient_tracker.Admission')),
                ('bed', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assignments', to='equipment.Bed')),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='bedassignment_creator', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-assigned_at'],
            },
        ),
        migrations.CreateModel(
            name='HealthSnapshotProxy',
            fields=[
            ],
            options={
                'verbose_name': 'Health Snapshot',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('patient_tracker.healthsnapshot',),
        ),
    ]
