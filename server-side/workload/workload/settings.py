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


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'v%^fldq-ctp7a6g6!ciw1p*_h7j!&3lxojj5(bm#kzwh*!s9^w'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


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
#    'south',

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


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', 
        'NAME': 'WORKLOAD_DB',
        'USER': 'WORKLOAD_USER',
        'PASSWORD': '0CHVezBAzq',
        'HOST': 'localhost',   # Or an IP Address that your DB is hosted on
        'PORT': '3306',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'



# Settings for shibboleth

SHIBBOLETH_ATTRIBUTE_MAP = {
   "HTTP_PERSISTENT_ID": (True, "username")
}

from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS
TEMPLATE_CONTEXT_PROCESSORS += (
   'shibboleth.context_processors.login_link',
   'shibboleth.context_processors.logout_link'
)

from django.conf.global_settings import AUTHENTICATION_BACKENDS
AUTHENTICATION_BACKENDS += (
  'shibboleth.backends.ShibbolethRemoteUserBackend',
)

LOGIN_URL = '/app/shib/login/'
SHIBBOLETH_LOGIN_URL  = 'https://survey.zqa.tu-dresden.de/Shibboleth.sso/Login'
SHIBBOLETH_LOGOUT_URL = 'https://survey.zqa.tu-dresden.de/Shibboleth.sso/Logout'
