"""
Django settings for project project.

Generated by 'django-admin startproject' using Django 2.2.3.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""
import datetime
import os

import django_heroku
import environ

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

from .utils import generate_secret

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

environ.Env.BOOLEAN_TRUE_STRINGS = ('true', 'on', 'ok', 'y', 'yes', '1', 'True')

env = environ.Env(
    # Set casting, default values
    PRODUCTION=(bool, False),
    TEST=(bool, False)
)

env_file = os.path.join(BASE_DIR, '.env')

if os.path.exists(env_file):
    environ.Env.read_env(env_file)
    print('Env file found and loaded')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env.str('SECRET_KEY', default='')

if SECRET_KEY == '':
    print('Warning! No secret key found. Using a one-shot generated key.')
    print('Please setup a SECRET_KEY value in your .env file.')
    SECRET_KEY = generate_secret()

# SECURITY WARNING: don't run with debug turned on in production!
PRODUCTION = env('PRODUCTION')
TEST = env('TEST')
DEV = not PRODUCTION and not TEST

DEBUG = not PRODUCTION

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'drf_yasg',
    'rest_framework',
    'corsheaders',

    'custom_auth',
    'api',
]

MIDDLEWARE = [
    'project.middlewares.HealthCheckMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'project.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DB_USER = env.str('POSTGRES_USER', default='')
DB_PASSWORD = env.str('POSTGRES_PASSWORD', default='')
DB_NAME = env.str('POSTGRES_DB', default='')
DB_HOST = env.str('POSTGRES_HOST', default='')

ALLOWED_HOSTS = env.str('ALLOWED_HOSTS', default='*').split(',')

DEFAULT_DB_STRING = f'psql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:5432/{DB_NAME}'

DATABASES = {
    'default': env.db('DATABASE_URL', default=DEFAULT_DB_STRING)
}

# Error tracking

SENTRY_SKIP = env.bool('SENTRY_SKIP', default=DEV)

if not SENTRY_SKIP:
    sentry_sdk.init(
        env.str('SENTRY_DSN'),
        integrations=[DjangoIntegration()],
        release=env.str('RELEASE')
    )

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissions'
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication'
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'SEARCH_PARAM': 'q',
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.NamespaceVersioning',
    'DEFAULT_VERSION': 'v1',
    'COERCE_DECIMAL_TO_STRING': False,
    'NON_FIELD_ERRORS_KEY': '__all__',
    'TEST_REQUEST_DEFAULT_FORMAT': 'json'
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': datetime.timedelta(minutes=10),
    'REFRESH_TOKEN_LIFETIME': datetime.timedelta(days=1)
}

AUTH_USER_MODEL = 'custom_auth.User'

# When using nginx as a proxy, the project should use the forwarded host header.
# This could mess with CSRF for instance when not set
USE_X_FORWARDED_HOST = env.bool('USE_X_FORWARDED_HOST', default=False)

# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/backend-static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/backend-media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

django_heroku.settings(locals())