"""
Django settings for snakd project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
PROJECT_APP_ROOT = os.path.abspath(BASE_DIR)
PROJECT_ROOT = os.path.abspath(os.path.dirname(PROJECT_APP_ROOT))
PUBLIC_ROOT = os.path.abspath(os.path.join(PROJECT_ROOT, 'public'))

# STATIC_ROOT = 'staticfiles'

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'ws-v4)b0r92@&alae894)(+6j#giv&-2uswqm=vg2oolm38f@e'

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
    'bootstrap3',
    'snakd',
    'snakd.apps.user',
    'snakd.apps.interest',
    'snakd.apps.chat',
    'scripts',
    'scripts.db_data'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'snakd.urls'

WSGI_APPLICATION = 'snakd.wsgi.application'

AUTHENTICATION_BACKENDS = ('snakd.apps.user.backends.EmailAuthBackend',)

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }


# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'

# Parse database configuration from $DATABASE_URL
import dj_database_url
# DATABASES['default'] =  dj_database_url.config()

# TODO HERE
# DATABASES['default'] = dj_database_url.config(default='postgres://USERNAME:PASSWORD@localhost/DBNAME')

DATABASES = {
    'default': dj_database_url.config(default='postgres://nznobbvumguuzd:6m8WRiKTl_Ze3d9mOPhaSuZ6Vy@ec2-50-16-190-77.compute-1.amazonaws.com:5432/dabedq5i48j024')
}

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
ALLOWED_HOSTS = ['*']


# Static files (CSS, JavaScript, Images)
STATICFILES_DIRS = [os.path.join(PROJECT_APP_ROOT, 'static')]

# template asset configuration
TEMPLATE_DIRS = [os.path.join(PROJECT_APP_ROOT, 'templates')]

# Email confirmation stuffs
from .email_settings import *
EMAIL_USE_TLS = EMAIL_USE_TLS
EMAIL_HOST = EMAIL_HOST
EMAIL_HOST_USER = EMAIL_HOST_USER
EMAIL_HOST_PASSWORD = EMAIL_HOST_PASSWORD
EMAIL_PORT = EMAIL_PORT

AUTH_USER_MODEL = "user.GenericUser"


# Django Postman Settings
POSTMAN_DISALLOW_ANONYMOUS = True # restrict messaging to a user-to-user exchange
POSTMAN_DISABLE_USER_EMAILING = True # change this eventually plz -DS
POSTMAN_AUTO_MODERATE_AS = True
AJAX_LOOKUP_CHANNELS = {
    'postman_users': dict(model="user.GenericUser", search_field='email'),
}
POSTMAN_AUTOCOMPLETER_APP = {
    'arg_default': 'postman_users',
}
