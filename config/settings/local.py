from config.settings.base import MIDDLEWARE

from .base import *

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'rome.sqlite3',
    }
}

## add an entry to MIDDLEWARE
MIDDLEWARE = MIDDLEWARE + ['config.middleware.turnstile_middleware.TurnstileMiddleware']

SECRET_KEY = '1234567890'
STATIC_URL = '/static/'

ALLOWED_HOSTS = ['*']
TTWR_COLLECTION_PID = (
    'test:5m6nkymr'  # TEMPORARILY-DISABLED -- overrides setting in base.py, which has the production-collection pid
)
