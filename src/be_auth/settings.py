import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# secrets
if 'POSTGRES_PASSWORD_FILE' in os.environ:
    with open(os.environ.get('POSTGRES_PASSWORD_FILE'), 'r', encoding='utf-8') as f:
        DB_PASSWORD = f.read()
else:
    DB_PASSWORD = 'please_use_env'
if 'DJANGO_SECRET_FILE' in os.environ:
    with open(os.environ.get('DJANGO_SECRET_FILE'), 'r', encoding='utf-8') as f:
        SECRET_KEY = f.read()
else:
    SECRET_KEY = 'please_use_env'
if 'JWT_SECRET_FILE' in os.environ:
    with open(os.environ.get('JWT_SECRET_FILE'), 'r', encoding='utf-8') as f:
        JWT_SECRET = f.read()
else:
    JWT_ALGORITHM = 'please_use_env'
JWT_ALGORITHM = 'HS256'
JWT_EXP_DELTA_SECONDS = 3600
if 'OAUTH_UID_FILE' in os.environ:
    with open(os.environ.get('OAUTH_UID_FILE'), 'r', encoding='utf-8') as f:
        OAUTH_UID = f.read()
else:
    OAUTH_UID = 'please_use_env'
if 'OAUTH_SECRET_FILE' in os.environ:
    with open(os.environ.get('OAUTH_SECRET_FILE'), 'r', encoding='utf-8') as f:
        OAUTH_SECRET = f.read()
else:
    OAUTH_SECRET = 'please_use_env'

# debug and host settings
DEBUG = os.environ.get('DEBUG', 'False') == 'True'
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost').split(',')
CSRF_TRUSTED_ORIGINS = [f"https://{u}" for u in os.environ.get('ALLOWED_HOSTS', 'localhost').split(',')]


# Application definition

INSTALLED_APPS = [
    # common db model
    'be_auth_model',
    # login - OAuth
    'oauth.apps.OauthConfig',
    # login - mfa
    'mfa.apps.MfaConfig',

    # admin page
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    # admin page
    # 'django.contrib.sessions.middleware.SessionMiddleware', 
    # 'django.contrib.auth.middleware.AuthenticationMiddleware', 
    # 'django.contrib.messages.middleware.MessageMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware'

    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'be_auth.urls'

TEMPLATES = [
    # admin page
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request', 
                'django.contrib.auth.context_processors.auth', 
                'django.contrib.messages.context_processors.messages'
            ],
        },
    },
]

WSGI_APPLICATION = 'be_auth.wsgi.application'


# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('POSTGRES_DB', 'be-auth'),
        'USER': os.environ.get('POSTGRES_USER', 'postgres'),
        'PASSWORD': DB_PASSWORD,
        'HOST': os.environ.get('POSTGRES_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '5432'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# admin page
STATIC_URL = 'auth/static/'
STATIC_ROOT = '/var/www/be-auth/static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


USE_X_FORWARDED_HOST = True
