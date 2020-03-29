# Generated by Django 3.0.4 on 2020-03-28 22:26

from django.db import migrations, models
import django.db.models.deletion
import patient_tracker.models


class Migration(migrations.Migration):

    dependencies = [
        ('patient_tracker', '0004_auto_20200328_2216'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignedbed',
            name='admission',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assigned_beds', to='patient_tracker.Admission'),
        ),
        migrations.AlterField(
            model_name='assignedbed',
            name='bed_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='beds_types_assigned', to='patient_tracker.BedType'),
        ),
    ]
