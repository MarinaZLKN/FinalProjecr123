import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-qq140cf!4$88b9dy9#8v0rs)xjkqsoz-ipi=b3wjuirkgmc9ul'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1']

AUTHENTICATION_BACKENDS = [

    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.flatpages',
    'fpages',
    'NewsPortal.apps.NewsportalConfig',
    'django_filters',
    'sign',
    'django_apscheduler',
    'protect',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',

    'django.middleware.locale.LocaleMiddleware',

    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
]

ROOT_URLCONF = 'NewsPaper.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'NewsPaper.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'ru'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

SITE_ID = 1

STATICFILES_DIRS = [
    BASE_DIR / "static"
]

LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/'

ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'

ACCOUNT_FORMS = {'signup': 'sign.models.CommonSignupForm'}

EMAIL_HOST = 'smtp.yandex.ru'
EMAIL_PORT = 465
EMAIL_HOST_USER = 'MarinaRAhven'
EMAIL_HOST_PASSWORD = 'reigoahven'
EMAIL_USE_SSL = True

DEFAULT_FROM_EMAIL = 'MarinaRAhven@yandex.ru'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

APSCHEDULER_DATETIME_FORMAT = "N j, Y, f:s a"
APSCHEDULER_RUN_NOW_TIMEOUT = 25


CELERY_BROKER_URL = 'redis://localhost:6379'
CELERY_RESULT_BACKEND = 'redis://localhost:6379'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': os.path.join(BASE_DIR, 'cache_files'),
    }
}
LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale')
]

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    #формат записи сообщений
    'formatters': {
        #В консоль должны выводиться сообщения  включающие время, уровень сообщения, сообщения
        'console_debug_format': {
            'format': '%(asctime)s %(levelname)s - %(message)s'
        },
        #Для сообщений WARNING и выше дополнительно должен выводиться путь к источнику события
        'console_warning_format': {
            'format': '%(asctime)s %(levelname)s - %(message)s - %(pathname)s'
        },
        #для сообщений ERROR и CRITICAL дополнительно должен выводить стэк ошибки
        'console_error_critical_format': {
            'format': '%(asctime)s %(levelname)s - %(message)s - %(pathname)s - %(exc_info)s'
        },
        #На почту должны отправляться сообщения  по формату, как в errors.log, но без стэка ошибок.
        'mail_format': {
            'format': '%(asctime)s %(levelname)s - %(message)s - %(pathname)s'
        },
        #Формат вывода предполагает время, уровень логирования, модуль и сообщение.
        'security_format': {
            'format': '%(asctime)s %(levelname)s - %(module)s - %(message)s'
        },
        #формат вывода с указанием времени, уровня логирования,
        # модуля, в котором возникло сообщение (аргумент module) и само сообщение.
        'general_log_format': {
            'format': '%(asctime)s %(levelname)s - %(module)s - %(message)s'
        },

    },
    #фильтры при разных значениях DEBUG
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
    },
    #Обработчики - то,куда сыпятся логи и как они обрабатываются
    'handlers': {
        #В консоль выводим сообщения DEBUG, WARNING, ERROR и CRITICAL
        'console': {
            'level': 'DEBUG', #уровень логирования
            'class': 'logging.StreamHandler', #самый простой класс, печатающий сообщения в консоль
            'formatter': 'console_debug_format', #формат логирования
            #фильтр, который пропускает записи в консоль только в случае, когда DEBUG = True
            'filters': ['require_debug_true'],
        },
        'console_warning': {
            'level': 'WARNING',
            'class': 'logging.StreamHandler',
            'formatter': 'console_warning_format',
        },
        'console_error_critical': {
            'level': 'ERROR',
            'class': 'logging.StreamHandler',
            'formatter': 'console_error_critical_format',
        },
        'general_file': {
            'class': "logging.FileHandler", #пeчатает сообщения в файл
            'filename': "general.log",
            'level': "INFO",#В файл general.log должны выводиться сообщения уровня INFO
            #пропускает запиаиси на почту и в файл general.log — только при DEBUG = False
            'filters': ['require_debug_false'],
            'formatter': 'general_log_format',
        },
        'errors_file': {
            'class': "logging.FileHandler",
            'filename': "errors.log",
            'level': "ERROR", #В файл errors.log должны выводиться сообщения только уровня ERROR и CRITICAL.
            'formatter': 'console_error_critical_format',
        },
        'security_file': {
            'class': "logging.FileHandler",
            'filename': "security.log", #В файл security.log должны попадать только сообщения, связанные с безопасностью
            'level': "WARNING", #Содержит информацию о предупреждениях системы.
            'formatter': 'security_format',
        },
        'mail_admins': {
            'level': 'ERROR', #На почту должны отправляться сообщения уровней ERROR и выше
            'class': 'django.utils.log.AdminEmailHandler',#обработчик, отправляющий данные сообщения по e-mail администратору
            'filters': ['require_debug_false'],#пропускает запиаиси на почту и в файл general.log — только при DEBUG = False
            'formatter': 'mail_format',
        },
    },
    # По сути то, что пишет в наши логи. Обьект для логирования сообщений
    'loggers': {
        'django': {
            'handlers': ['console', 'console_warning', 'console_error_critical'],
            'propagate': True, #Этим параметром регулируется возможность передачи сообщения другим логгерам.
            # Если оно установлено в False то дальше сообщение не пойдет.
        },
        #На почту должны отправляться сообщения уровней ERROR и выше из django.request и django.server
        'django.request': {
            'handlers': ['mail_admins', 'errors_file'],
            'level': 'ERROR',  #если регистратор определен с уровнем ERROR, то в него попадут только сообщения ERROR и CRITICAL
            'propagate': False,
        },
        #На почту должны отправляться сообщения уровней ERROR и выше из django.request и django.server
        'django.server': {
            'handlers': ['mail_admins', 'errors_file'],
            'level': 'ERROR',
            'propagate': False,
        },
        #В файл error.log должны попадать сообщения только из логгеров django.request, django.server, django.template, django.db_backends.
        'django.db_backends': {
            'handlers': ['errors_file'],
            'level': 'ERROR',
            'propagate': False,
        },
        'django.template': {
            'handlers': ['errors_file'],
            'level': 'ERROR',
            'propagate': False,
        },
        #В файл security.log должны попадать только сообщения, связанные с безопасностью, а значит только из логгера django.security
        'django.security': {
            'handlers': ['security_file'],
            'level': 'WARNING',
            'propagate': False,
        }
    }
}