import json

from .base import *

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

SECRET_KEY = get_env_setting('SECRET_KEY')
STATIC_URL = '/projects/rome/static/'
ALLOWED_HOSTS = ['library.brown.edu']
EMAIL_HOST = get_env_setting('EMAIL_HOST')
SERVER_EMAIL = get_env_setting('SERVER_EMAIL')
