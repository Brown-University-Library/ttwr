from .base import *  # noqa: F403
from .base import get_env_setting

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
SERVER_EMAIL = get_env_setting('SERVER_EMAIL')

## turnstile settings ---------------------------
TURNSTILE_SITE_KEY = get_env_setting('TURNSTILE_SITE_KEY')
TURNSTILE_SECRET_KEY = get_env_setting('TURNSTILE_SECRET_KEY')
TURNSTILE_API_URL = get_env_setting('TURNSTILE_API_URL')
TURNSTILE_API_TIMEOUT = get_env_setting('TURNSTILE_API_TIMEOUT')
TURNSTILE_API_MAX_RETRIES = get_env_setting('TURNSTILE_API_MAX_RETRIES')
TURNSTILE_API_RETRY_DELAY = get_env_setting('TURNSTILE_API_RETRY_DELAY')


