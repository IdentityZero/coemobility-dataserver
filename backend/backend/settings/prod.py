import os
from .base import *

SECRET_KEY = os.environ["DJANGO_SECRET_KEY"]
DEBUG = False

# Added localhost
ALLOWED_HOSTS = ['122.248.192.233', 'localhost', 'coemobility.com']

EVENTSTREAM_ALLOW_ORIGINS = ['*']
CORS_ALLOWED_ORIGINS = [
    'https://122.248.192.233',
    'https://122.248.192.233',
    'https://localhost',
    'https://coemobility.com',
]

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