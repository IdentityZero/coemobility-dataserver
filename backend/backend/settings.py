"""
Django settings for backend project.

Generated by 'django-admin startproject' using Django 5.0.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-6^rf01*bh!h^ucz1e&g(y21o*pn*+h%mq&@-&5dx(ofu&tsfl1"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Added localhost
ALLOWED_HOSTS = ['122.248.192.233', 'localhost', 'coemobility.com']


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "daphne", # Place this below
    "django.contrib.staticfiles",

    "rest_framework",
    "rest_framework.authtoken",
    "channels",
    'corsheaders',
    "django_eventstream",

    "Users",
    "Vehicles",
    "Parking",
    "Api",
    "WebAPI",
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "backend.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "backend.wsgi.application"
ASGI_APPLICATION = "backend.asgi.application"
EVENTSTREAM_ALLOW_ORIGINS = ['*']
CORS_ALLOWED_ORIGINS = [
    '*',
]

# EVENTSTREAM_ALLOW_ORIGINS = ['http://192.168.100.144:8002',
#     'http://192.168.100.144:8000',]


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "myParking",
        "USER" : "admin",
        "PASSWORD": "DAjCjeCsjckolfJcbkY2",
        "HOST": "coemobilitydb.cpks4sm0udv9.ap-southeast-1.rds.amazonaws.com",
        "PORT": 3306,
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "America/Los_Angeles" # This is the identifier for PST
USE_TZ = False

USE_I18N = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = "/static/"
# Remove this already since we dont input user data through this server

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = "/media/"

DEFAULT_PROFILE_IMAGE = "profile_pics/profile.png"
PROFILE_IMAGE_LOG_FILE = os.path.join(MEDIA_ROOT,"profile_pics\profile_pics.csv")

DEFAULT_VEHICLE_IMAGE = "vehicle_pics/vehicle.png"
VEHICLE_IMAGE_LOG_FILE = os.path.join(MEDIA_ROOT,"vehicle_pics/vehicle_pics.csv")

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

REDIS_HOST = 'localhost'
REDIS_PORT = 6379
