"""
Django settings for ytbl project.

Generated by 'django-admin startproject' using Django 3.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# common
APP_ROOT_NAME = "ytbl"  # APP_ROOT_NAME 은 편의를 위해 추가한 변수임.
SITE_DOMAIN = "hovak.world"

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SECRET_KEY")

# SGIS API KEY
SGIS_CONSUMER_KEY = os.environ.get("SGIS_CONSUMER_KEY")
SGIS_CONSUMER_SECRET = os.environ.get("SGIS_CONSUMER_SECRET")

# VWORLD API KEY
VWORLD_KEY = os.environ.get("VWORLD_KEY")


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = [
    "localhost",
    SITE_DOMAIN
]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'map',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ytbl.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = f'{APP_ROOT_NAME}.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": os.environ.get("POSTGRES_DB"),
        "USER": os.environ.get("POSTGRES_USER"),
        "PASSWORD": os.environ.get("POSTGRES_PASSWORD"),
        "HOST": os.environ.get("POSTGRES_HOST"),
        "PORT": os.environ.get("POSTGRES_PORT"),
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


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'ko'

TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = "/static/"
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]  # 기본적인 참조 외에 collectstatic 시 추가할 static file 경로. 기본적으로 각 앱의 하위의 /static/ 폴더를 참조함.
STATIC_ROOT = os.path.join(BASE_DIR, "static_collected")

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Logging
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {"format": "[%(levelname)s] %(asctime)s %(module)s %(message)s"},
        "action": {"format": "[%(levelname)s] %(asctime)s %(ip)s %(user_pk)s %(username)s %(request_method)s %(view_name)s %(message)s %(status_code)s"},
        "ip": {"format": "[%(levelname)s] %(asctime)s %(ip)s %(request_method)s %(message)s"},
    },
    "handlers": {
        "console": {"level": "DEBUG", "class": "logging.StreamHandler", "formatter": "standard"},
        "logfile": {
            "level": "INFO",
            "class": "logging.handlers.RotatingFileHandler",
            "maxBytes": 1024 * 1024 * 10,  # 로그 파일 당 10M 까지
            "backupCount": 10,  # 로그 파일을 최대 10개까지 유지
            # 'class': 'logging.FileHandler',
            "filename": f"/var/log/django/{APP_ROOT_NAME}.log",
            "formatter": "standard",
        },
        "actionLogfile": {
            "level": "INFO",
            "class": "logging.handlers.RotatingFileHandler",
            "maxBytes": 1024 * 1024 * 10,  # 로그 파일 당 10M 까지
            "backupCount": 10,  # 로그 파일을 최대 10개까지 유지
            "filename": "/var/log/django/action.log",
            "formatter": "action",
        },
        "disallowedHost": {
            "level": "ERROR",
            "class": f"{APP_ROOT_NAME}.loggers.DisallowedHostLogHandler",
            "formatter": "ip",
        },
    },
    "loggers": {
        "default": {
            "level": "DEBUG",  # 로거의 기본 레벨. 이 레벨이 우선시 된다.
            "handlers": [
                "logfile",
            ],
        },
        "action": {
            "level": "DEBUG",
            "handlers": [
                "actionLogfile",
            ],
        },
        "django.security.DisallowedHost": {
            "level": "ERROR",
            "handlers": ["disallowedHost"],
            "propagate": False,  # 최상위 로거까지 전파 여부
        },
    },
}
