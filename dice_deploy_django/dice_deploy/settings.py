"""
Django settings for dice_deploy project.

Generated by "django-admin startproject" using Django 1.8.5.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

import os
from kombu import Queue, Exchange
from cfy_wrapper.exceptions import CfyMockupSuccess, CfyMockupFail

IS_TEST_SETTINGS = False

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = "np$u5a4u$rh-or%ibtladssbbrf26d(y4k+m_alh@r2hdebgiq"

DEBUG = True
ALLOWED_HOSTS = []

INSTALLED_APPS = (
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.staticfiles",
    "rest_framework",
    "rest_framework_swagger",
    "cfy_wrapper",
    "cfy_wrapper_gui",
    "djcelery",
)

MIDDLEWARE_CLASSES = (
)

API_DATE_FORMAT = '%Y-%m-%d'
API_TIME_FORMAT = '%H:%M:%S'
API_DT_FORMAT = '%sT%s' % (API_DATE_FORMAT, API_TIME_FORMAT)

REST_FRAMEWORK = {
    "DEFAULT_RENDERER_CLASSES": (
        "rest_framework.renderers.JSONRenderer",
    ),
    "DEFAULT_PARSER_CLASSES": (
        "rest_framework.parsers.JSONParser",
        "rest_framework.parsers.MultiPartParser",
        "rest_framework.parsers.FileUploadParser",
    ),
    "DATETIME_FORMAT": API_DT_FORMAT
}

ROOT_URLCONF = "dice_deploy.urls"
WSGI_APPLICATION = "dice_deploy.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
    }
}

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Celery config
BROKER_URL = 'amqp://'
CELERY_TASK_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_ENABLE_UTC = True
CELERY_DEFAULT_QUEUE = 'dice_deploy'
CELERY_QUEUES = (
    # consumed by main worker
    Queue('dice_deploy', Exchange('dice_deploy'), routing_key='dice_deploy'),
    # consumed by test worker (unit tests)
    Queue('dice_deploy_tests', Exchange('dice_deploy_tests'), routing_key='dice_deploy_tests'),
)
CELERYD_POOL_RESTARTS = True

# Cloudify settings
CFY_MANAGER_URL = "172.16.95.126"
POOL_SLEEP_INTERVAL = 3  # In seconds

# Cloudify mockup settings
MOCKUP_CFY_OPTION_NO = None  # don't mockup
MOCKUP_CFY_OPTION_YES_SUCCESS = CfyMockupSuccess()
MOCKUP_CFY_OPTION_YES_FAIL = CfyMockupFail()
MOCKUP_CFY = MOCKUP_CFY_OPTION_NO  # selected option

# File upload storage
MEDIA_ROOT = os.path.join(BASE_DIR, "uploads")

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,

    'formatters': {
        'verbose': {
            'format': "[%(asctime)s] %(levelname)s "
                      "[%(name)s:%(lineno)s] %(message)s",
            'datefmt': "%Y-%m-%d %H:%M:%S"
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': 'app.log',
            'formatter': 'verbose',
        },
        'file_tasks': {
            'class': 'logging.FileHandler',
            'filename': 'tasks.log',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'views': {
            'handlers': ['console', 'file'],
            'propagate': False,
            'level': 'DEBUG',
        },
        'tasks': {
            'handlers': ['console', 'file_tasks'],
            'propagate': False,
            'level': 'DEBUG',
        },
    },
}

STATIC_URL = '/static/'

# angular configuration
ANGULAR_ENDPOINT = '/'

# Local overrides
try:
    from dice_deploy.local_settings import *
except ImportError:
    pass
