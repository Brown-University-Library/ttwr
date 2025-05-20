import os

from django.core.exceptions import ImproperlyConfigured


def get_env_setting(setting):
    """Get the environment setting or return exception"""
    try:
        return os.environ[setting]
    except KeyError:
        error_msg = 'Set the %s env variable' % setting
        raise ImproperlyConfigured(error_msg.encode('utf8'))


BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

MIDDLEWARE = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.contrib.messages.context_processors.messages',
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.request',
            ]
        },
    },
]

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'crispy_forms',
    'markdown_deux',
    'pagedown',
    'rome_app',
)

TIME_ZONE = 'America/New_York'

USE_TZ = True

ROOT_URLCONF = 'config.urls'

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

STATIC_ROOT = os.path.normpath(os.path.join(BASE_DIR, 'assets'))

MEDIA_ROOT = os.path.normpath(os.path.join(BASE_DIR, 'media'))

CRISPY_TEMPLATE_PACK = 'bootstrap3'

MARKDOWN_DEUX_STYLES = {
    'default': {
        'extras': {
            'code-friendly': None,
            'footnotes': None,
        },
        'safe_mode': 'escape',
    },
}

LOG_DIR = get_env_setting('LOG_DIR')
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            # 'format': '%(asctime)s %(levelname)s %(message)s'
            'format': '[%(asctime)s] %(levelname)s [%(module)s-%(funcName)s()::%(lineno)d] %(message)s',
            'datefmt': '%d/%b/%Y %H:%M:%S',
        },
    },
    'filters': {'require_debug_false': {'()': 'django.utils.log.RequireDebugFalse'}},
    'handlers': {
        'mail_admins': {'level': 'ERROR', 'filters': ['require_debug_false'], 'class': 'django.utils.log.AdminEmailHandler'},
        'log_file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(LOG_DIR, 'rome.log'),
            'formatter': 'verbose',
        },
        'null': {
            'class': 'logging.NullHandler',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
        'django.security': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
        'django.security.DisallowedHost': {
            'handlers': ['null'],  # do nothing for disallowed hosts errors
            'propagate': False,
        },
        'rome': {
            'handlers': ['log_file'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}

TTWR_COLLECTION_PID = 'bdr:240509'  # ID: 621
