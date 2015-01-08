import os
import logging
import logging.handlers

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
XLINK_NAMESPACE = 'http://www.w3.org/1999/xlink'

def setup_logger(filename):
    '''Configures a logger to write to console & <filename>.'''
    formatter = logging.Formatter(u'%(asctime)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(u'logger')
    logger.setLevel(logging.DEBUG)
    file_handler = logging.handlers.RotatingFileHandler(filename, maxBytes=5000000, backupCount=5)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    return logger

app_dir = os.path.dirname(os.path.abspath(__file__))
logger = setup_logger(os.path.join(app_dir, 'ttwr.log'))

