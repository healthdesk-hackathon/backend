# Generated by Django 3.0.4 on 2020-03-28 11:26

from django.db import migrations

from custom_auth.utils import get_user_model


def create_admin(apps, schema_editor):
    User = get_user_model()
    User.objects.create_superuser('admin', '352MaAehYJJu')


class Migration(migrations.Migration):

    dependencies = [
        ('custom_auth', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_admin)
    ]