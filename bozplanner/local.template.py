import sys
import os

# Generate a value for this key by using the following command in a python interpreter:
# from django.utils.crypto import get_random_string; print(get_random_string(50, "abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)"))
SECRET_KEY = None

# Turn off debug in a production environment
DEBUG = True

ALLOWED_HOSTS = []

WSGI_APPLICATION = 'bozplanner.wsgi.application'

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

STATIC_URL = '/static/'

USE_DJANGOSAML2 = False

WEBCAL_BASE = 'bozplanner.pieterbos.me'

if SECRET_KEY is None:
    print("Please edit the values in your local setup.")
    sys.exit(1)

if DEBUG and DATABASES['default']['ENGINE'] != 'django.db.backends.sqlite3':
    print("Debug configurations must run with a local database")
    sys.exit(1)
