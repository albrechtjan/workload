"""
Django settings for workload project.

This is the most important settings file.
If deines the confuguration of the django project,
as well as the configurations of the apps belonging to the 
django project.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Django requires a secret key for cryptography
# Because the settings.py file is committed to the git repository and not kept to a very high level of secrecy, 
# the secret key is stored in a seperate file and loaded from there.
with open('/home/ks/secret_key_django.txt') as f:
    SECRET_KEY = f.read().strip()

# SECURITY WARNING: don't run with debug turned on in production!
# You can set these options to True to get very helpful error messages when Django hits a problem on page load.
DEBUG = False
TEMPLATE_DEBUG = False

ALLOWED_HOSTS = [".tu-dresden.de",".tu-dresden.de."]


# Application definition

INSTALLED_APPS = (
    # these are django core apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # This is "our" app, the one which has the user-frontend and the web API.
    'workloadApp',
    # The shibboleth app is documented here: https://github.com/KonstantinSchubert/django-shibboleth-adapter.
    # It provides a middleware for Shibboleth Authentication.
    'shibboleth',

)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'shibboleth.middleware.ShibbolethRemoteUserMiddleware', # https://github.com/KonstantinSchubert/django-shibboleth-adapter
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'workload.urls'
WSGI_APPLICATION = 'workload.wsgi.application'


# Databse settings

# Because the settings.py file is committed to the git repository,
# we do not want to include the database password here. It should be
# stored in another location in the server and can be loaded from there.
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


# https://docs.djangoproject.com/en/1.9/howto/static-files/
STATIC_URL = '/static/'
STATIC_ROOT = "/var/www/static/"

#########################################################################################################
# Settings for the workloadApp django app 


# Unfortunately, the app currently makes the assumption that there are two semesters 
# per year with the same start dates every year.

SUMMER_SEMESTER_START_MONTH = 4
SUMMER_SEMESTER_START_DAY_OF_MONTH = 1
WINTER_SEMESTER_START_MONTH = 10
WINTER_SEMESTER_START_DAY_OF_MONTH = 1

##########################################################################################################
# Settings for the django-shibboleth-adapter https://github.com/KonstantinSchubert/django-shibboleth-adapter

# This is the shibboleth attribute that is used to identify the user. 
# The apps backend.py implements a method called `clean_username` which extracts a substring from this attribute 
# which then becomes the actual user key. Depending on the user key that is used, this method must be 
# updated.
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
##########################################################################################################

# Settings for logging
# https://docs.djangoproject.com/en/1.9/topics/logging/
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
            # Edit here if you want to change the logging level
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': '/home/ks/workload/workload.log',
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
