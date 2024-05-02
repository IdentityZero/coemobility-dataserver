import os
import json
from .base import *

with open('/etc/backend_config.json', 'r') as config_file:
    config = json.load(config_file)

SECRET_KEY = config['SECRET_KEY']
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
        "NAME": config["DB_NAME"],
        "USER" : config["DB_USER"],
        "PASSWORD": config["DB_PASSWORD"],
        "HOST": config["DB_HOST"],
        "PORT": 3306,
    }
}