# Generated by Django 3.0.4 on 2020-03-28 21:40

from django.db import migrations, models
import django.db.models.deletion
import patient_tracker.models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('patient_tracker', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BedType',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('total', models.IntegerField()),
            ],
        ),
        migrations.RemoveField(
            model_name='admission',
            name='submission',
        ),
        migrations.CreateModel(
            name='OutOfServiceBed',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('when_out_of_service', models.DateTimeField(auto_now_add=True)),
                ('reason', models.CharField(choices=[('cleaning', 'cleaning'), ('equip fail', 'equipment failure'), ('unavailable', 'unavailable'), ('other', 'other')], max_length=20)),
                ('bed_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='out_of_service_beds', to='patient_tracker.BedType')),
            ],
        ),
        migrations.CreateModel(
            name='AssignedBed',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, validators=[patient_tracker.models.prevent_update])),
                ('waiting_since', models.DateTimeField(auto_now_add=True)),
                ('admission', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='assigned_bed', to='patient_tracker.Admission')),
                ('bed_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='assigned_beds', to='patient_tracker.BedType', validators=[patient_tracker.models.AssignedBed.validate_bed_type_available])),
                ('waiting_for_bed_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='waiting_for_assigned_beds', to='patient_tracker.BedType')),
            ],
        ),
    ]
