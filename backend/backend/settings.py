"""
Django settings for backend project.

Generated by 'django-admin startproject' using Django 5.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""
from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Add new apps here
APP_DIRS = [
    os.path.join(BASE_DIR, "User"),
    os.path.join(BASE_DIR, "Friends"),
]

TEMPLATE_DIRS = [os.path.join(app, 'templates') for app in APP_DIRS if os.path.exists(os.path.join(app, 'templates'))]

FILE_UPLOAD_MAX_MEMORY_SIZE = 2097152
DATA_UPLOAD_MAX_MEMORY_SIZE = 2097152

FILE_UPLOAD_HANDLERS = [
    'django.core.files.uploadhandler.MemoryFileUploadHandler',
    'django.core.files.uploadhandler.TemporaryFileUploadHandler',
]

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-^6z#%nf*!6vj*+*nxf^-+qq!by6&zb7_7u8r$_t-6+u#$5o$j='

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'corsheaders', #Added for CORS header configuration
    'rest_framework',
    'backend',
	'channels',
	'daphne',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Backend apps here
    'User',
    'Friends',
	'Tokens',
	'Match',
	'Player',
	'Tournament',
	'pong',
	'stats',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware', #Has to be before CommonMiddleware
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': TEMPLATE_DIRS,
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

#WSGI_APPLICATION = 'backend.wsgi.application'
ASGI_APPLICATION = 'backend.asgi.application'
# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('POSTGRES_DB'),
        'USER':  os.environ.get('POSTGRES_USER'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
        'HOST': os.environ.get('DB_HOST'),
        'PORT': 5432,
    }
}

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default database-backed sessions
SESSION_ENGINE = 'django.contrib.sessions.backends.db'
SESSION_COOKIE_AGE = 60 * 100 # session expiration time (in seconds)
SESSION_COOKIE_HTTPONLY = False # Set to True in production
SESSION_COOKIE_SECURE = False  # Set to True in production
SESSION_COOKIE_SAMESITE = 'Lax' #set to 'Lax' in production

# our custom User model
AUTH_USER_MODEL = 'User.User'

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',  # Default authentication backend
]

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Helsinki'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

#CSRF settings

CSRF_COOKIE_SAMESITE = 'Lax' #set to 'Lax' in production
CSRF_COOKIE_HTTPONLY = False #set to true in production
CSRF_COOKIE_SECURE = False #set to true in production

CSRF_TRUSTED_ORIGINS = [
		'http://localhost:80',
		'http://127.0.0.1:80',
		'http://localhost',
		'http://127.0.0.1',
		'https://localhost',
		'https://127.0.0.1',
		'https://localhost:443',
		'https://127.0.0.1:443'
]

#CORS settings

CORS_ALLOW_HEADERS = [ "accept", "referer", "accept-encoding", "authorization", "content-type", "dnt", "origin", "user-agent", "X-CSRFToken", "x-sessionid", "x-requested-with"]
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOWED_ORIGINS = [
		'http://localhost:80',
		'http://127.0.0.1:80',
		'http://localhost',
		'http://127.0.0.1',
		'https://localhost',
		'https://127.0.0.1',
		'https://localhost:443',
		'https://127.0.0.1:443'
]


# SSL Settings

# SECURE_SSL_REDIRECT = True # uncomment in production
