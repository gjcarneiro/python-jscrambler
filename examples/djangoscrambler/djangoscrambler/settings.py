"""
Django settings for djangoscrambler project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""
from __future__ import absolute_import

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import json

BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '6z8&zzc2w5-04l#l@pdm-6xtm!wgw3b!1)fgjq7r$p*vchu=x3'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.staticfiles',

     # Adding the 'jscrambler' app will enable the management command
     # 'scramblestatic', which should be executed after
     # 'collectstatic': it takes all .js file under STATIC_ROOT, sends
     # them to jscrambler, and replaces it with a scrambled version.
    'jscrambler',

    # This is our demo app.
    'scramble',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'djangoscrambler.urls'

WSGI_APPLICATION = 'djangoscrambler.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
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

STATIC_ROOT = os.path.join(BASE_DIR, "staticroot", "static")

#
# Read a jscramble configuration file, place the result into the
# JSCRAMBLER_CONFIG setting.
#
config_file_name = os.path.join(BASE_DIR,"..", "config.json")
with open(config_file_name, "r") as configfile:
    JSCRAMBLER_CONFIG = json.load(configfile)
if os.path.exists(config_file_name + ".local"):
    with open(config_file_name + ".local", "r") as configfile:
        JSCRAMBLER_CONFIG.update(json.load(configfile))
del config_file_name

JSCRAMBLER_CONFIG["filesSrc"] = ["**/*.js"]
