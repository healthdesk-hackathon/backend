# Generated by Django 3.0.4 on 2020-03-28 13:18

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('submission', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CommonSymptoms',
            fields=[
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
            ],
        ),
        migrations.CreateModel(
            name='GradedSymptoms',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('difficulty_breathing', models.IntegerField(validators=[django.core.validators.MaxValueValidator(10), django.core.validators.MinValueValidator(0)])),
                ('anxious', models.IntegerField(validators=[django.core.validators.MaxValueValidator(10), django.core.validators.MinValueValidator(0)])),
            ],
        ),
        migrations.CreateModel(
            name='OverallWellbeing',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('overall_value', models.IntegerField(validators=[django.core.validators.MaxValueValidator(10), django.core.validators.MinValueValidator(0)])),
            ],
        ),
        migrations.CreateModel(
            name='PersonalData',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other/Prefer not to disclose')], max_length=1)),
                ('date_of_birth', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='RelatedConditions',
            fields=[
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
            ],
        ),
        migrations.RenameModel(
            old_name='Master',
            new_name='Patient',
        ),
        migrations.RemoveField(
            model_name='admission',
            name='submission_id',
        ),
        migrations.RemoveField(
            model_name='phone',
            name='submission_id',
        ),
        migrations.RemoveField(
            model_name='submission',
            name='master_id',
        ),
        migrations.AddField(
            model_name='admission',
            name='submission',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='admissions', to='submission.Submission'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='phone',
            name='submission',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='phones', to='submission.Submission'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='submission',
            name='patient',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='submissions', to='submission.Patient'),
        ),
        migrations.AlterField(
            model_name='submission',
            name='identifier',
            field=models.CharField(max_length=50),
        ),
        migrations.DeleteModel(
            name='Person',
        ),
        migrations.AddField(
            model_name='relatedconditions',
            name='submission',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='related_conditions', to='submission.Submission'),
        ),
        migrations.AddField(
            model_name='personaldata',
            name='submission',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='personal_data', to='submission.Submission'),
        ),
        migrations.AddField(
            model_name='overallwellbeing',
            name='submission',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='overall_wellbeing', to='submission.Submission'),
        ),
        migrations.AddField(
            model_name='gradedsymptoms',
            name='submission',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='graded_symptoms', to='submission.Submission'),
        ),
        migrations.AddField(
            model_name='commonsymptoms',
            name='submission',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='common_symptoms', to='submission.Submission'),
        ),
    ]
