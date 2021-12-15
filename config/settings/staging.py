from .base import *

DEBUG = True

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
EMAIL_HOST = get_env_setting('EMAIL_HOST')
ALLOWED_HOSTS = [get_env_setting('ALLOWED_HOST')]
TTWR_COLLECTION_PID = 'test:5m6nkymr'
