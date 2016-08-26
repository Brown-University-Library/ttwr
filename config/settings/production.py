from .base import *
import json

DEBUG = False

ADMINS = json.loads(get_env_setting('ADMINS_JSON'))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': get_env_setting('DB_NAME'),
        'USER': get_env_setting('DB_USER'),
        'PASSWORD': get_env_setting('DB_PASSWORD'),
        'HOST': get_env_setting('DB_HOST'),
        'PORT': get_env_setting('DB_PORT'),
    }
}

SECRET_KEY = get_env_setting('SECRET_KEY')
