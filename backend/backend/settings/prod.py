import os
import json
from .base import *

with open('/etc/backend_config.json', 'r') as config_file:
    config = json.load(config_file)

SECRET_KEY = config['SECRET_KEY']
DEBUG = False

# Added localhost
ALLOWED_HOSTS = ['47.129.54.22', 'localhost','127.0.0.1', 'coemobility.com']

EVENTSTREAM_ALLOW_ORIGINS = ['*']
CORS_ALLOWED_ORIGINS = [
    'http://47.129.54.22',
    'https://47.129.54.22',
    'http://localhost',
    'http://127.0.0.1',
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