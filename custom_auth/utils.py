from django.contrib.auth import get_user_model as base_get_user_model

from custom_auth.models import User as CustomUser


# Simple helper to get custom user model with correct typing
def get_user_model() -> CustomUser:
    return base_get_user_model()


def setup_auth_test_data():
    User = get_user_model()

    User.objects.create_superuser('admin', 'admin@test.local', 'admin_pass')
    User.objects.create_user('user', 'user@test.local', 'user_pass')
