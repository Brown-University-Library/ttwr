import json

from config.settings.base import *  # noqa: F403
from config.settings.base import MIDDLEWARE, get_env_setting

DEBUG = False

ADMINS = json.loads(get_env_setting('ADMINS_JSON'))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'OPTIONS': {
            'charset': 'utf8mb4',
        },
        'NAME': get_env_setting('DB_NAME'),
        'USER': get_env_setting('DB_USER'),
        'PASSWORD': get_env_setting('DB_PASSWORD'),
        'HOST': get_env_setting('DB_HOST'),
        'PORT': get_env_setting('DB_PORT'),
    }
}

## add an entry to MIDDLEWARE
MIDDLEWARE = MIDDLEWARE + ['config.middleware.turnstile_middleware.TurnstileMiddleware']

SECRET_KEY = get_env_setting('SECRET_KEY')
STATIC_URL = '/projects/rome/static/'
ALLOWED_HOSTS = ['library.brown.edu']
EMAIL_HOST = get_env_setting('EMAIL_HOST')
SERVER_EMAIL = get_env_setting('SERVER_EMAIL')

## turnstile settings ---------------------------
TURNSTILE_SITE_KEY = get_env_setting('TURNSTILE_SITE_KEY')
TURNSTILE_SECRET_KEY = get_env_setting('TURNSTILE_SECRET_KEY')
TURNSTILE_API_URL = get_env_setting('TURNSTILE_API_URL')
TURNSTILE_API_TIMEOUT = int(get_env_setting('TURNSTILE_API_TIMEOUT'))
TURNSTILE_EMAIL = get_env_setting('TURNSTILE_EMAIL')
TURNSTILE_SESSION_EXPIRY_MINUTES = int(get_env_setting('TURNSTILE_SESSION_EXPIRY_MINUTES'))
TURNSTILE_ALLOWED_IPS = json.loads(get_env_setting('TURNSTILE_ALLOWED_IPS_JSON'))
