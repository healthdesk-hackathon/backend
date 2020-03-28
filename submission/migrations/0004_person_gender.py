# Generated by Django 3.0.4 on 2020-03-28 12:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('submission', '0003_auto_20200328_1140'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='gender',
            field=models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other/Prefer not to disclose')], default='O', max_length=1),
            preserve_default=False,
        ),
    ]
