from .base import *

SECRET_KEY = "django-insecure-6^rf01*bh!h^ucz1e&g(y21o*pn*+h%mq&@-&5dx(ofu&tsfl1"
DEBUG = True

# Added localhost
ALLOWED_HOSTS = ['localhost']

EVENTSTREAM_ALLOW_ORIGINS = ['*']
CORS_ALLOWED_ORIGINS = [
    'http://localhost',
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}
