import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# secrets
assert 'POSTGRES_PASSWORD_FILE' in os.environ, 'POSTGRES PASSWORD FILE NOT GIVEN'
with open(os.environ.get('POSTGRES_PASSWORD_FILE'), 'r') as f:
  DB_PASSWORD = f.read()
assert 'DJANGO_SECRET_FILE' in os.environ, 'DJANGO SECRET FILE NOT GIVEN'
with open(os.environ.get('DJANGO_SECRET_FILE'), 'r') as f:
  SECRET_KEY = f.read()
assert 'JWT_SECRET_FILE' in os.environ, 'JWT SECRET FILE NOT GIVEN'
with open(os.environ.get('JWT_SECRET_FILE'), 'r') as f:
  JWT_SECRET = f.read()
JWT_ALGORITHM = 'HS256'
JWT_EXP_DELTA_SECONDS = 3600
assert 'OAUTH_UID_FILE' in os.environ, 'OAUTH UID FILE NOT GIVEN'
with open(os.environ.get('OAUTH_UID_FILE'), 'r') as f:
  OAUTH_UID = f.read()
assert 'OAUTH_SECRET_FILE' in os.environ, 'OAUTH SECRET FILE NOT GIVEN'
with open(os.environ.get('OAUTH_SECRET_FILE'), 'r') as f:
  OAUTH_SECRET = f.read()

# debug and host settings
DEBUG = os.environ.get('DEBUG', 'False') == 'True'
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost').split(',')


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
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

ROOT_URLCONF = 'be_auth.urls'

TEMPLATES = [
]

WSGI_APPLICATION = 'be_auth.wsgi.application'


# Database
DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': BASE_DIR / 'db.sqlite3',
    # }
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
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


USE_X_FORWARDED_HOST = True