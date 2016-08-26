from .base import *

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'rome.sqlite3',
    }
}

SECRET_KEY = '1234567890'
STATIC_URL = '/static/'
