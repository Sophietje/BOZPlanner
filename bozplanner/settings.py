"""Global project settings"""
import os
import sys
import djcelery

from django.utils.formats import iter_format_modules

# Determine available modules
try:
    from bozplanner import local
except ImportError:
    print("If you just cloned the project, you need to copy local.template.py to local.py and edit the values for your local setup.")
    raise

if local.USE_DJANGOSAML2:
    try:
        import djangosaml2
        HAVE_DJANGOSAML2 = True
    except ImportError:
        HAVE_DJANGOSAML2 = False
else:
    HAVE_DJANGOSAML2 = False

try:
    import debug_toolbar
    HAVE_DEBUG_TOOLBAR = True
except ImportError:
    HAVE_DEBUG_TOOLBAR = False

# Project base path
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# Localization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = False

DATE_INPUT_FORMATS = ['%d-%m-%Y']
DATETIME_INPUT_FORMATS = ["%d-%m-%Y+%H:%M"]

DATE_FORMAT = 'd-m-Y'
DATETIME_FORMAT = 'd-m-Y H:i'
SHORT_DATE_FORMAT = DATE_FORMAT
SHORT_DATETIME_FORMAT = DATETIME_FORMAT

# Authentication
LOGIN_URL = '/saml2/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

AUTH_USER_MODEL = "members.Person"

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

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]

if HAVE_DJANGOSAML2:
    AUTHENTICATION_BACKENDS = [
        'members.auth.SAML2Backend'
    ] + AUTHENTICATION_BACKENDS

# Project apps
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'djcelery',
    'kombu.transport.django',
    'djcelery_email',

    'members',
    'meetings',
    'help',
    'bozplanner',
    'django_extensions',
]

if HAVE_DJANGOSAML2:
    INSTALLED_APPS += [
        'djangosaml2',
    ]

if HAVE_DEBUG_TOOLBAR and local.DEBUG:
    INSTALLED_APPS += [
        'debug_toolbar',
    ]

# Email settings
EMAIL_BACKEND = 'djcelery_email.backends.CeleryEmailBackend'
BROKER_URL = 'django://'
EMAIL_HOST = 'smtp.utwente.nl'
EMAIL_HOST_USER = 'bozplanner@utwente.nl'

djcelery.setup_loader()

# Middlewares
MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Views
ROOT_URLCONF = 'bozplanner.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'builtins': [
                'django.templatetags.i18n',
                'bozplanner.templatetags.misc',
            ],
        },
    },
]

# Local settings
try:
    from bozplanner.local import *
except ImportError:
    print("If you just cloned the project, you need to copy local.template.py to local.py and edit the values for your local setup.")
    raise
