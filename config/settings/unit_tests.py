from .base import *

DEBUG = True

ADMINS = (
    ('random', 'random@example.com'),
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'unit_tests.sqlite3',
    }
}

SECRET_KEY = '1234567890'
STATIC_URL = '/static/'
