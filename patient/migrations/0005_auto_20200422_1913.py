# Generated by Django 3.0.5 on 2020-04-22 19:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0004_auto_20200419_1350'),
    ]

    operations = [
        migrations.AlterField(
            model_name='personaldata',
            name='patient',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='personal_data', to='patient.Patient'),
        ),
    ]