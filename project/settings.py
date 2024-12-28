"""Django settings for the project."""
from datetime import timedelta
from environs import Env
import os
from pathlib import Path


env = Env()
env.read_env()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = env.str('SECRET_KEY')

DEBUG = env.bool('DEBUG')

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS')

# Приложения Django
DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

# Внешние библиотеки
EXTERNAL_LIBS = [ 
    'debug_toolbar',
    'django_celery_beat',
    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_simplejwt',
    'djoser',
]

# Внешние библиотеки
EXTERNAL_LIBS_MUST_BE_FIRST = [
    'jazzmin',    
]

# Приложения самого проекта
PROJECT_APPS = [
    'accounts.apps.AccountsConfig',
    'simple_auth.apps.SimpleAuthConfig',
]

INSTALLED_APPS = EXTERNAL_LIBS_MUST_BE_FIRST + DJANGO_APPS + EXTERNAL_LIBS + PROJECT_APPS


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

ROOT_URLCONF = 'project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
        ],
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

WSGI_APPLICATION = 'project.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': env.str('DB_NAME'),
        'USER': env.str('DB_USER'),
        'PASSWORD': env.str('DB_PASS'),
        'HOST': env.str('DB_HOST'),
        'PORT': env('DB_PORT'),
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

LANGUAGE_CODE = 'ru-RU'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'templates/static'),
]

AUTH_USER_MODEL = 'accounts.User'

if DEBUG:
    INTERNAL_IPS = ALLOWED_HOSTS

# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_HOST = env.str('EMAIL_HOST')
EMAIL_PORT = env('EMAIL_PORT')
EMAIL_USE_SSL = env.bool('EMAIL_USE_SSL')
EMAIL_HOST_PASSWORD = env.str('EMAIL_HOST_PASSWORD')
EMAIL_HOST_USER = env.str('EMAIL_HOST_USER')
DEFAULT_FROM_EMAIL = env.str('DEFAULT_FROM_EMAIL')

# Настройки Redis
REDIS_HOST = env.str('REDIS_HOST')
REDIS_PORT = env('REDIS_PORT')

# Настройки Celery
CELERY_BROKER_URL = f'redis://{REDIS_HOST}:{REDIS_PORT}/0'
CELERY_RESULT_BACKEND = f'redis://{REDIS_HOST}:{REDIS_PORT}/0'


# Настройки REST_FRAMEWORK
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
}

# Настройки JWT
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),  # Время жизни access токена
    'REFRESH_TOKEN_LIFETIME': timedelta(days=5),    # Время жизни refresh токена
    'ROTATE_REFRESH_TOKENS': False,                 # Поворот токенов при обновлении
    'BLACKLIST_AFTER_ROTATION': True,               # Черный список токенов после поворота
    'UPDATE_LAST_LOGIN': False,                     # Обновление времени последнего входа

    'ALGORITHM': 'HS256',                           # Алгоритм шифрования
    'SIGNING_KEY': SECRET_KEY,                      # Ключ подписи
    'VERIFYING_KEY': None,                          # Ключ верификации
    'AUDIENCE': None,                               # Аудитория
    'ISSUER': None,                                 # Издатель

    'AUTH_HEADER_TYPES': ('JWT',),                  # Тип заголовка авторизации
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',       # Имя заголовка авторизации
    'USER_ID_FIELD': 'email',                       # Поле пользователя для идентификации
    'USER_ID_CLAIM': 'email',                       # Утверждение пользователя для идентификации

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),  # Классы токенов
    'TOKEN_TYPE_CLAIM': 'token_type',               # Утверждение типа токена

    'JTI_CLAIM': 'jti',                             # Утверждение JTI

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',  # Утверждение времени жизни скользящего токена
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),    # Время жизни скользящего токена
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),  # Время жизни обновления скользящего токена
}


# Настройки DJOSER
DJOSER = {
    'PASSWORD_RESET_CONFIRM_URL': 'password/reset/confirm/{uid}/{token}',
    'USERNAME_RESET_CONFIRM_URL': 'username/reset/confirm/{uid}/{token}',
    'ACTIVATION_URL': 'activate/{uid}/{token}',
    'SEND_ACTIVATION_EMAIL': True,
}
