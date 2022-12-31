"""
Django settings for DjangoWebsite project.

Generated by 'django-admin startproject' using Django 3.2.14.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
import json
import os
import sys
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.

BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!

with open(os.path.join(BASE_DIR, "config.json"), "r") as f:
    _config = json.load(f)

TURNSTILE_DEFAULT_CONFIG = {
    'theme': 'light',
}

if all(_config.values()):
    TURNSTILE_SITEKEY = _config["TURNSTILE_SITEKEY"]
    TURNSTILE_SECRET = _config["TURNSTILE_SECRET"]
    HCAPTCHA_SITEKEY = _config["HCAPTCHA_SITEKEY"]
    HCAPTCHA_SECRET = _config["HCAPTCHA_SECRET"]
SECRET_KEY = _config["SECRET_KEY"] or "django-insecure-#l#3ps7+(*+7f#0cz=aj-sp!6$-waaf6h=*+=5h*(5njj_^)@8"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
AUTH_USER_MODEL = 'user.User'
ALLOWED_HOSTS = _config["ALLOWED_HOSTS"]

# Application definition
APPLICATIONS_CONFIG_FILE = "config.json"
BASE_APPLICATION_DIR = os.path.join(BASE_DIR, "applications")
APPLICATIONS_DIR = [f"applications.{app_path}" for app_path in os.listdir(BASE_APPLICATION_DIR)
                    if os.path.isdir(os.path.join(BASE_APPLICATION_DIR, app_path)) and app_path != "__pycache__"
                    and os.path.isfile(os.path.join(BASE_APPLICATION_DIR, app_path, APPLICATIONS_CONFIG_FILE))]

INSTALLED_APPS = [
    'simpleui',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'dwebsocket',
    'turnstile',
    'hcaptcha',
    'imagekit',
    'user',
    'oauth',
    'im',
    'files',
    'geoip',
    'monitor',
]
INSTALLED_APPS += APPLICATIONS_DIR[:]

#  appHandler.app_settings(): django.core.exceptions.AppRegistryNotReady: Apps aren't loaded yet.

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'monitor.middleware.MonitorMiddleware.MonitorMiddleware',
]

ROOT_URLCONF = 'DjangoWebsite.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'builtins': [
                'django.templatetags.static'
            ],
        },
    },
]

WSGI_APPLICATION = 'DjangoWebsite.wsgi.application'
# WEBSOCKET_FACTORY_CLASS = 'dwebsocket.backends.uwsgi.factory.uWsgiWebSocketFactory'

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

IS_CONTAINER = True
# Container: Do not have MySQL & Redis, Production environment
# Go to Zh-Website Replit Page: https://Zh-Website.zmh-program.repl.co/
if IS_CONTAINER:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }

    # Cache
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
            'LOCATION': 'website-cache',
        }
    }
else:
    DATABASES = {
        'default':
            {
                'ENGINE': 'django.db.backends.mysql',  # module
                'NAME': 'django-database',  # database name
                'HOST': 'localhost',  # ip
                'PORT': 3306,
                'USER': 'root',
                'PASSWORD': 'zmh200904',
            }
    }

    # Cache
    CACHES = {
        "default": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": "redis://127.0.0.1:6379/",
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
            }
        }
    }
# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

SIMPLEUI_CONFIG = {
    'system_keep': True,
    'menus': [
        {
            'name': '仪表盘',
            'icon': 'fa-solid fa-gauge-high',
            'url': '/monitor/',
            'codename': 'monitor',
        },

        {
            'name': '用户数据',
            'icon': 'fa-solid fa-globe',
            'url': '/geoip/',
            'codename': 'geoip',
        },

        {
            'name': '文件管理',
            'icon': 'fa-regular fa-copy',
            'url': '/files/',
            'codename': 'fileManager',
        },

        {
            'name': 'Github 主页',
            'icon': 'fab fa-github',
            'url': 'https://zmh-program.github.io/',
            'codename': 'GithubPage'
        }
    ],
}

# Encode / Decode
CODING = "utf-8"
WS_INTERVAL = 0.04
# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'zh-hans'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static & Media files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/
LOGIN_URL = '/login/'
STATIC_URL = '/static/'
MEDIA_URL = '/media/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]
STATIC_ROOT = os.path.join(BASE_DIR, "/static/")
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

#  File Settings
FILE_DATABASE_DIR = os.path.join(BASE_DIR, "files", "database")
MAX_FILE_NAME_LENGTH = 30
FILE_CACHE_CAPABILITY = 50
FILE_PAGINATION = 10  # nums per page
FILE_PERMISSION_LEVEL = 2
SIZE_UNIT = 1024
MAX_FILE_SIZE = (1024 ** 2) * 10  # 10 MiB

# GeoIP Settings
GEOIP_RELEASE_INTERVAL = 60 * 60 * 6  # 6 hours
GEOIP_DATABASE_FILE = os.path.join(BASE_DIR, "geoip", "database", "geolite.mmdb")

# JWT Settings
TOKEN_VALID_TIME = 60 * 3  # unit: seconds

# Monitor Settings
MONITOR_INTERVAL = 1  # 1 second

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# AUTO DETECTION! DO NOT CHANGED! (run manage.py -> False, gunicorn wsgi.py -> True)
IS_DEPLOYED = True

DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 8000
