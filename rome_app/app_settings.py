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
BDR_IDENTITY = get_env_setting('ROME_BDR_IDENTITY')
BDR_AUTH_CODE = get_env_setting('ROME_BDR_AUTH_CODE')
BDR_POST_URL = 'https://%s/api/items/v1/' % BDR_SERVER
XLINK_NAMESPACE = 'http://www.w3.org/1999/xlink'
BDR_ANNOTATION_URL = 'https://%s/services/getMods/' % BDR_SERVER
