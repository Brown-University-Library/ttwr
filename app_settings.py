import os

from django.core.exceptions import ImproperlyConfigured
def get_env_setting(setting):
    try:
        return os.environ[setting]
    except KeyError:
        error_msg = "Set the %s env variable" % setting
        raise ImproperlyConfigured(error_msg)

BDR_SERVER = get_env_setting('ROME_BDR_SERVER')
PID_PREFIX = get_env_setting('ROME_PID_PREFIX')
BOOKS_PER_PAGE = 20
BDR_ADMIN = 'BROWN:DEPARTMENT:LIBRARY:REPOSITORY'
BDR_IDENTITY = get_env_setting('ROME_BDR_IDENTITY')
BDR_AUTH_CODE = get_env_setting('ROME_BDR_AUTH_CODE')
BDR_POST_URL = 'https://%s/api/items/v1/' % BDR_SERVER
