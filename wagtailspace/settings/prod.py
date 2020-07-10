"""
This file is configured for hosting on codered.cloud.
See: https://www.codered.cloud/docs/django/environment/
"""

import os

from .base import *


# Do not set SECRET_KEY, Postgres or LDAP password or any other sensitive data here.
# Instead, use environment variables or create a local.py file on the server.

# Disable debug mode
DEBUG = False
TEMPLATES[0]['OPTIONS']['debug'] = False


# -- Recommended CodeRed Cloud settings ---------------------------------------

ALLOWED_HOSTS = [os.environ['VIRTUAL_HOST']]

SECRET_KEY = os.environ['RANDOM_SECRET_KEY']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'HOST': os.environ['DB_HOST'],
        'NAME': os.environ['DB_NAME'],
        'USER': os.environ['DB_USER'],
        'PASSWORD': os.environ['DB_PASSWORD'],
        'OPTIONS': {'sslmode': 'require'},
    }
}

# Use CodeRed's included email service, or replace this with your own.
EMAIL_BACKEND = 'django_sendmail_backend.backends.EmailBackend'

# -- End CodeRed Cloud settings -----------------------------------------------


# Configuration from environment variables
# Alternatively, you can set these in a local.py file on the server

env = os.environ.copy()

# Basic configuration

BASE_URL = 'http://%s' % env['VIRTUAL_HOST']

if 'SERVER_EMAIL' in env:
    SERVER_EMAIL = env['SERVER_EMAIL']
else:
    SERVER_EMAIL = 'noreply@%s' % env['VIRTUAL_HOST']

DEFAULT_FROM_EMAIL = SERVER_EMAIL

if 'CACHE_PURGE_URL' in env:
    INSTALLED_APPS += ('wagtail.contrib.wagtailfrontendcache', )
    WAGTAILFRONTENDCACHE = {
        'default': {
            'BACKEND': 'wagtail.contrib.wagtailfrontendcache.backends.HTTPBackend',
            'LOCATION': env['CACHE_PURGE_URL'],
        },
    }

# Logging

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
        },
    },
    'formatters': {
        'default': {
            'verbose': '[%(asctime)s] (%(process)d/%(thread)d) %(name)s %(levelname)s: %(message)s'
        }
    },
    'loggers': {
        'wagtailspace': {
            'handlers':     [],
            'level':        'INFO',
            'propagate':    False,
            'formatter':    'verbose',
        },
        'wagtail': {
            'handlers':     [],
            'level':        'INFO',
            'propagate':    False,
            'formatter':    'verbose',
        },
        'django.request': {
            'handlers':     ['mail_admins'],
            'level':        'ERROR',
            'propagate':    False,
            'formatter':    'verbose',
        },
        'django.security': {
            'handlers':     ['mail_admins'],
            'level':        'ERROR',
            'propagate':    False,
            'formatter':    'verbose',
        },
    },
}


# CodeRed Cloud provides normal rotated log files in /var/log/
LOG_DIR = os.path.join(os.path.abspath("/"), "var", "log")

# Wagtail Space log
LOGGING['handlers']['wagtailspace_file'] = {
    'level':        'INFO',
    'class':        'logging.FileHandler',
    'filename':     os.path.join(LOG_DIR, 'wagtailspace.log'),
}
LOGGING['loggers']['wagtail']['handlers'].append('wagtailspace_file')

# Wagtail log
LOGGING['handlers']['wagtail_file'] = {
    'level':        'INFO',
    'class':        'logging.FileHandler',
    'filename':     os.path.join(LOG_DIR, 'wagtail.log'),
}
LOGGING['loggers']['wagtail']['handlers'].append('wagtail_file')

# Error log
LOGGING['handlers']['errors_file'] = {
    'level':        'ERROR',
    'class':        'logging.FileHandler',
    'filename':     os.path.join(LOG_DIR, 'error.log'),
}
LOGGING['loggers']['django.request']['handlers'].append('errors_file')
LOGGING['loggers']['django.security']['handlers'].append('errors_file')


WEBPACK_LOADER['DEFAULT']['CACHE'] = not DEBUG
WEBPACK_LOADER['DEFAULT']['STATS_FILE'] = os.path.join(BASE_DIR, 'config-prd-stats.json')
