# Generated by Django 3.0.4 on 2020-04-04 20:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient_tracker', '0006_healthsnapshotfile'),
    ]

    operations = [
        migrations.AddField(
            model_name='healthsnapshot',
            name='main_complain',
            field=models.CharField(blank=True, default='', max_length=250, null=True),
        ),
    ]