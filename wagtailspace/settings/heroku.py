import os
import dj_database_url
import django_heroku

from .base import *

# Do not set SECRET_KEY, Postgres or LDAP password or any other sensitive data here.
# Instead, use environment variables or create a local.py file on the server.

# Disable debug mode
DEBUG = False
TEMPLATES[0]['OPTIONS']['debug'] = False

# Compress static files offline and minify CSS
# http://django-compressor.readthedocs.org/en/latest/settings/#django.conf.settings.COMPRESS_OFFLINE
COMPRESS_OFFLINE = True
COMPRESS_CSS_FILTERS = [
    'compressor.filters.css_default.CssAbsoluteFilter',
    'compressor.filters.cssmin.CSSMinFilter',
]
COMPRESS_CSS_HASHING_METHOD = 'content'

# Configuration from environment variables
# Alternatively, you can set these in a local.py file on the server

env = os.environ.copy()

# Basic configuration

APP_NAME = env.get('APP_NAME', 'wagtailspace')
SECRET_KEY = env['SECRET_KEY']

if 'PRIMARY_HOST' in env:
    BASE_URL = 'http://%s/' % env['PRIMARY_HOST']

if 'SERVER_EMAIL' in env:
    SERVER_EMAIL = env['SERVER_EMAIL']

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


if 'LOG_DIR' in env:
    # Wagtail Space log
    LOGGING['handlers']['wagtailspace_file'] = {
        'level':        'INFO',
        'class':        'cloghandler.ConcurrentRotatingFileHandler',
        'filename':     os.path.join(env['LOG_DIR'], 'wagtailspace.log'),
        'maxBytes':     5242880,  # 5MB
        'backupCount':  5
    }
    LOGGING['loggers']['wagtail']['handlers'].append('wagtailspace_file')

    # Wagtail log
    LOGGING['handlers']['wagtail_file'] = {
        'level':        'INFO',
        'class':        'cloghandler.ConcurrentRotatingFileHandler',
        'filename':     os.path.join(env['LOG_DIR'], 'wagtail.log'),
        'maxBytes':     5242880,  # 5MB
        'backupCount':  5
    }
    LOGGING['loggers']['wagtail']['handlers'].append('wagtail_file')

    # Error log
    LOGGING['handlers']['errors_file'] = {
        'level':        'ERROR',
        'class':        'cloghandler.ConcurrentRotatingFileHandler',
        'filename':     os.path.join(env['LOG_DIR'], 'error.log'),
        'maxBytes':     5242880,  # 5MB
        'backupCount':  5
    }
    LOGGING['loggers']['django.request']['handlers'].append('errors_file')
    LOGGING['loggers']['django.security']['handlers'].append('errors_file')


if 'EMAIL_HOST' in env:
    EMAIL_HOST = env['EMAIL_HOST']
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True
if 'EMAIL_HOST_USER' in env:
    EMAIL_HOST_USER = env['EMAIL_HOST_USER']
if 'EMAIL_HOST_PASSWORD' in env:
    EMAIL_HOST_PASSWORD = env['EMAIL_HOST_PASSWORD']


WEBPACK_LOADER['DEFAULT']['CACHE'] = not DEBUG
WEBPACK_LOADER['DEFAULT']['STATS_FILE'] = os.path.join(BASE_DIR, 'config-prd-stats.json')

django_heroku.settings(locals())
