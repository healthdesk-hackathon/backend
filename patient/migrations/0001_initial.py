# Generated by Django 3.0.5 on 2020-04-12 13:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('identifier', models.CharField(max_length=50)),
                ('id_type', models.CharField(max_length=50)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='patient_creator', to=settings.AUTH_USER_MODEL)),
                ('modifier', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='patient_modifier', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created'],
            },
        ),
        migrations.CreateModel(
            name='Phone',
            fields=[
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('phone_number', models.CharField(max_length=50)),
                ('phone_type', models.CharField(max_length=10)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='phone_creator', to=settings.AUTH_USER_MODEL)),
                ('modifier', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='phone_modifier', to=settings.AUTH_USER_MODEL)),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='phones', to='patient.Patient')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PersonalData',
            fields=[
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other/Prefer not to disclose')], max_length=1)),
                ('date_of_birth', models.DateField()),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='personaldata_creator', to=settings.AUTH_USER_MODEL)),
                ('modifier', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='personaldata_modifier', to=settings.AUTH_USER_MODEL)),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='personal_data', to='patient.Patient')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PatientPhoto',
            fields=[
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('photo', models.ImageField(upload_to='patient_photos')),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='patientphoto_creator', to=settings.AUTH_USER_MODEL)),
                ('modifier', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='patientphoto_modifier', to=settings.AUTH_USER_MODEL)),
                ('patient', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='patient_photo', to='patient.Patient')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='NextOfKinContact',
            fields=[
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('title', models.CharField(max_length=20)),
                ('relationship', models.CharField(choices=[('WIFE', 'Wife'), ('HUSBAND', 'Husband'), ('CHILD', 'Child'), ('PARENT', 'Parent'), ('LEGAL GUARDIAN', 'Legal Guardian'), ('OTHER', 'Other')], max_length=20)),
                ('other_relationship', models.CharField(blank=True, max_length=20, null=True)),
                ('phone_number', models.CharField(max_length=50)),
                ('notes', models.TextField()),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='nextofkincontact_creator', to=settings.AUTH_USER_MODEL)),
                ('modifier', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='nextofkincontact_modifier', to=settings.AUTH_USER_MODEL)),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='next_of_kin_contacts', to='patient.Patient')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
