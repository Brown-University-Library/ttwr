import os

from .base import *  # noqa: F403 -- imports settings necessary for run_tests.py

DEBUG = True

ADMINS = (('random', 'random@example.com'),)

DATABASES = {
    'default': {
        'ENGINE': os.getenv('TEST_DB_ENGINE', 'django.db.backends.sqlite3'),
        'NAME': os.getenv('TEST_DB_NAME', 'unit_tests.sqlite3'),
    }
}

SECRET_KEY = '1234567890'
STATIC_URL = '/static/'
