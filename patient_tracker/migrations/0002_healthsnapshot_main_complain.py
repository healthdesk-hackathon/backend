# Generated by Django 3.0.5 on 2020-05-02 20:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient_tracker', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='healthsnapshot',
            name='main_complain',
            field=models.CharField(blank=True, default='', max_length=250, null=True),
        ),
    ]