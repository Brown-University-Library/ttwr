import os
import pathlib
import pprint

import dotenv

from .base import *  # noqa: F403 -- imports settings necessary for run_tests.py

## Load environment variables from .env file
dotenv_path = pathlib.Path(__file__).parent.parent.parent / '../.env_unit_tests'
# if not dotenv_path.exists():
#     raise ImproperlyConfigured(f'dotenv file not found at {dotenv_path}')  # commented out so github-ci doesn't fail
dotenv.read_dotenv(dotenv_path, override=True)


DEBUG = True

ADMINS = (('random', 'random@example.com'),)

# DATABASES = {
#     'default': {
#         'ENGINE': os.getenv('TEST_DB_ENGINE', 'django.db.backends.sqlite3'),
#         'NAME': os.getenv('TEST_DB_NAME', 'unit_tests.sqlite3'),
#         'USER': os.getenv('TEST_DB_USER'),
#         'PASSWORD': os.getenv('TEST_DB_PASSWORD'),
#         'HOST': os.getenv('TEST_DB_HOST'),
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': os.getenv('DB_ENGINE', 'django.db.backends.sqlite3'),
        'TEST': {
            'ENGINE': os.getenv('TEST_DB_ENGINE', 'django.db.backends.sqlite3'),
            'NAME': os.getenv('TEST_DB_NAME', 'unit_tests.sqlite3'),
            'USER': os.getenv('TEST_DB_USER'),
            'PASSWORD': os.getenv('TEST_DB_PASSWORD'),
            'HOST': os.getenv('TEST_DB_HOST'),
            'PORT': os.getenv('TEST_DB_PORT'),
        },
    }
}
pprint.pprint(DATABASES)

SECRET_KEY = '1234567890'
STATIC_URL = '/static/'
