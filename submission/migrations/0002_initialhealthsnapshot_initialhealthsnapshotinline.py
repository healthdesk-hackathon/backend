# Generated by Django 3.0.5 on 2020-04-04 09:10

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
            name='InitialHealthSnapshotInline',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='InitialHealthSnapshot',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
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
                ('submission', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='initial_health_snapshot', to='submission.Submission')),
            ],
        ),
    ]
