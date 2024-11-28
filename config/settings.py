import os
from datetime import timedelta
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(dotenv_path='.env.prod')

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

DEBUG = os.getenv('DJANGO_DEBUG', False).lower() == 'true'

ALLOWED_HOSTS = list(os.getenv('DJANGO_ALLOWED_HOSTS'))

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

LANGUAGE_CODE = 'ru'
TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_TZ = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

ROOT_URLCONF = 'config.urls'

WSGI_APPLICATION = 'config.wsgi.application'


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'habits.tasks': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}


if DEBUG:
    CORS_ALLOW_ALL_ORIGINS = True
else:
    CORS_ALLOWED_ORIGINS = os.getenv('CORS_ALLOWED_ORIGINS', '').split(',')

INSTALLED_APPS = [
    'rest_framework',
    'rest_framework_simplejwt',
    'django_extensions',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'drf_yasg',
    'corsheaders',
    'users',
    'habits',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',

    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ]
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
}

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

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.getenv('POSTGRES_DB'),
        'USER': os.getenv('POSTGRES_USER'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD'),
    }
}

CACHES_ENABLED = os.getenv('DJANGO_CACHES_ENABLED', False).lower() == 'true'
if CACHES_ENABLED:
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.redis.RedisCache",
            "LOCATION": os.getenv('REDIS_LOCATION'),
        }
    }

AUTH_USER_MODEL = 'users.User'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL')
CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND')
CELERY_TIMEZONE = os.getenv('CELERY_TIMEZONE')
CELERY_TASK_TRACK_STARTED = os.getenv('CELERY_TASK_TRACK_STARTED', False).lower() == 'true'
CELERY_TASK_TIME_LIMIT = 30 * 60

CELERY_BEAT_SCHEDULE = {
    'send-habit-reminders-every-minute': {
        'task': 'habits.tasks.check_habit_reminders',
        'schedule': timedelta(seconds=30),
    },
}

CELERY_TASK_ALWAYS_EAGER = os.getenv('CELERY_TASK_ALWAYS_EAGER', False).lower() == 'true'

CELERY_EAGER_PROPAGATES_EXCEPTIONS = os.getenv('CELERY_EAGER_PROPAGATES_EXCEPTIONS', False).lower() == 'true'
