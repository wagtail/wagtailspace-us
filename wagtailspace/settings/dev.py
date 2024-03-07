from .base import *

DEBUG = True
TEMPLATES[0]['OPTIONS']['debug'] = True
AUTH_PASSWORD_VALIDATORS = []

INSTALLED_APPS += [
    'wagtail.contrib.styleguide',
]

ALLOWED_HOSTS = ['*']

BASE_URL = 'http://localhost:8000'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'wagtailspace-us',
        'USER': 'postgres',
        'HOST': 'localhost',
        'PASSWORD': 'postgres',
    }
}

SECRET_KEY = 'Not a secret!!!'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    }
}

INTERNAL_IPS = '127.0.0.1'

try:
    from .local import *
except ImportError:
    pass
