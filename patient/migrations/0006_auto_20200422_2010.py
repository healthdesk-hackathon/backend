# Generated by Django 3.0.5 on 2020-04-22 20:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0005_auto_20200422_1913'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patientidentifier',
            name='patient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='patient_identifiers', to='patient.Patient'),
        ),
    ]
