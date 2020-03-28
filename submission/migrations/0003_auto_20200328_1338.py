# Generated by Django 3.0.4 on 2020-03-28 13:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('submission', '0002_auto_20200328_1318'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commonsymptoms',
            name='submission',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='common_symptoms', to='submission.Submission'),
        ),
        migrations.AlterField(
            model_name='gradedsymptoms',
            name='submission',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='graded_symptoms', to='submission.Submission'),
        ),
        migrations.AlterField(
            model_name='overallwellbeing',
            name='submission',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='overall_wellbeing', to='submission.Submission'),
        ),
        migrations.AlterField(
            model_name='relatedconditions',
            name='submission',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='related_conditions', to='submission.Submission'),
        ),
    ]
