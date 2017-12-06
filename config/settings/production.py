from .base import *
import json

DEBUG = False

ADMINS = json.loads(get_env_setting('ADMINS_JSON'))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES,NO_ZERO_DATE,NO_ZERO_IN_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER'",
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
