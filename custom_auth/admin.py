from django.contrib.auth.admin import UserAdmin

from custom_auth.models import User
from project.admin import admin_site

admin_site.register(User, UserAdmin)
