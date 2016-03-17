"""
Django settings for workload project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


with open('/home/ks/secret_key_django.txt') as f:
    SECRET_KEY = f.read().strip()

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
TEMPLATE_DEBUG = False

ALLOWED_HOSTS = [".tu-dresden.de",".tu-dresden.de."]


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'workloadApp',
    'shibboleth',

)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'shibboleth.middleware.ShibbolethRemoteUserMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'workload.urls'
WSGI_APPLICATION = 'workload.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

with open('/home/ks/WORKLOAD_DB_PASSWORD.txt') as f:
    WORKLOAD_DB_PASSWORD = f.read().strip()

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', 
        'NAME': 'WORKLOAD_DB',
        'USER': 'WORKLOAD_USER',
        'PASSWORD': WORKLOAD_DB_PASSWORD,
        'HOST': 'localhost',   # Or an IP Address that your DB is hosted on
        'PORT': '3306',
    }
}

CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


STATIC_URL = '/static/'
STATIC_ROOT = "/var/www/static/"




# Settings for shibboleth
SHIBBOLETH_USER_KEY = "persistent-id"
SHIBBOLETH_ATTRIBUTE_LIST = []

from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS
TEMPLATE_CONTEXT_PROCESSORS += (
   'shibboleth.context_processors.login_link',
   'shibboleth.context_processors.logout_link'
)

from django.conf.global_settings import AUTHENTICATION_BACKENDS
AUTHENTICATION_BACKENDS += (
  'workloadApp.backends.CustomShibboBackend',
)

LOGIN_URL = '/app/shib/login/'
SHIBBOLETH_LOGIN_URL  = 'https://survey.zqa.tu-dresden.de/Shibboleth.sso/Login'
SHIBBOLETH_LOGOUT_URL = 'https://survey.zqa.tu-dresden.de/Shibboleth.sso/Logout'
SHIBBOLETH_LOGOUT_REDIRECT_URL = "https://survey.zqa.tu-dresden.de/" # this is not actually respected by the current shibboleth installation of TU Dresden
SHIBBOLETH_DJANGO_SESSION_MAY_OUTLIVE_SHIBBOLETH_SESSION = True #we want to keep the users logged in even if the session cookie of shibboleth is gone.


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format' : "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt' : "%d/%b/%Y %H:%M:%S"
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': '/home/ks/workload/mysite.log',
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'django': {
            'handlers':['file'],
            'propagate': True,
            'level':'DEBUG',
        },
        'workloadApp': {
            'handlers': ['file'],
            'level': 'DEBUG',
        },
    }
}