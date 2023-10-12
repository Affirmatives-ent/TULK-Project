from pathlib import Path
from decouple import config
from datetime import timedelta
from dotenv import load_dotenv
import os
from django.db.models import Q
from django.contrib.auth import get_user_model
import django_heroku
import dj_database_url

import cloudinary.uploader
import cloudinary.api
import cloudinary_storage
import cloudinary


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ['SECRET']
ALLOWED_HOSTS = [os.environ['WEBSITE_HOSTNAME']]
CSRF_TRUSTED_ORIGINS = ['https://' + os.environ['WEBSITE_HOSTNAME']]

# ALLOWED_HOSTS = ["*"]

# SECRET_KEY = config("SECRET_KEY")

# # SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = config("DEBUG", cast=bool)

# ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    "corsheaders",
    "rest_framework_simplejwt",
    "rest_framework_simplejwt.token_blacklist",
    "drf_spectacular",
    'cloudinary_storage',
    'cloudinary',
    'accounts',
    'user_groups',
    'posts',
    'article',
    'chat',


]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    "corsheaders.middleware.CorsMiddleware",
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'backendAPI.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

# Replace 'project_name' with your project's name


WSGI_APPLICATION = 'backendAPI.wsgi.application'

# Use the in-memory channel layer for development
# CHANNEL_LAYERS = {
#     'default': {
#         'BACKEND': 'channels.layers.InMemoryChannelLayer',
#     },
# }


# ROOT_URLCONF = 'backendAPI.urls'  # Replace 'project_name' with your project's name


load_dotenv()
# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }


# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': 'Tulk_Social_DB',
#         'USER': 'postgres',
#         'PASSWORD': 'Payboi10',
#         'HOST': 'localhost',
#         'PORT': '5432',
#     }
# }

connection_string = os.environ.get('AZURE_POSTGRESQL_CONNECTIONSTRING')
if connection_string:
    parameters = {pair.split('=')[0]: pair.split('=')[1]
                  for pair in connection_string.split()}

    # Check if 'user' parameter is present
    if 'user' in parameters:
        user = parameters['user']
    else:
        # Handle the case where 'user'
        user = None

    if 'password' in parameters:
        password = parameters['password']
    else:
        # Handle the case where 'password' parameter
        password = None

    if 'dbname' in parameters:
        dbname = parameters['dbname']
    else:
        # Handle the case where 'dbname' parameter is missing
        dbname = None

    if 'host' in parameters:
        host = parameters['host']
    else:
        # Handle the case where 'host' parameter is missing
        host = None

    if 'port' in parameters:
        port = parameters['port']
    else:
        # Handle the case where 'port' parameter is missing
        port = None
else:
    # Handle the case where the environment variable is not set
    user = None
    password = None
    dbname = None
    host = None
    port = None

# Use the extracted parameters in your database configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': dbname,
        'USER': user,
        'PASSWORD': password,
        'HOST': host,
        'PORT': port,
    }
}


# MY_SENDCHAMP_PUBLIC_KEY = os.getenv('SENDCHAMP_KEY')
SENDCHAMP_KEY = os.getenv('SENDCHAMP_KEY')
DEBUG = os.getenv('DEBUG')
# print("SENDCHAMP_KEY:", SENDCHAMP_KEY)
print("Hello world!")


# cloudinary.config(
#     cloud_name="hyklbuwof",
#     api_key=os.getenv('CLOUDINARY_API_KEY'),
#     api_secret=os.getenv('CLOUDINARY_API_SECRET'),
# )


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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


REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        "rest_framework.permissions.IsAuthenticatedOrReadOnly",
    ),
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",

    ),
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",

    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
}


SPECTACULAR_SETTINGS = {
    "TITLE": "Tulk API Project",
    "DESCRIPTION": "Tulk Social",
    "VERSION": "1.0.0",
    # OTHER SETTINGS
}


AUTHENTICATION_BACKENDS = [
    'accounts.authentications.CustomAuthBackend',
    'django.contrib.auth.backends.ModelBackend',
]
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True

CORS_ORIGIN_WHITELIST = (
    "http://localhost:3000",
    "http://localhost:8000",
)

SIMPLE_JWT = {
    'AUTH_HEADER_TYPES': ('Bearer',),
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=120),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=90),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'ACCESS_TOKEN_ALGORITHM': 'HS256',  # Specify the algorithm for access tokens
    'REFRESH_TOKEN_ALGORITHM': 'HS256',  # Specify the algorithm for refresh tokens
    'SIGNING_KEY': SECRET_KEY
}


# DJOSER = {
#     'USER_ID_FIELD': 'phone_number',
#     'LOGIN_FIELD': 'phone_number',
# }
# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

MAX_OTP_TRY = 3

MIN_PASSWORD_LENGTH = 8
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

# Check if running on Heroku
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Use django.contrib.staticfiles.storage.StaticFilesStorage for local development on Windows
# else:
#     STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': "djwh3low0",
    'API_KEY': os.getenv('CLOUDINARY_API_KEY'),
    'API_SECRET': os.getenv('CLOUDINARY_API_SECRET'),
}

DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

# WHITENOISE_KEEP_ONLY_HASHED_FILES = True
# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field
# settings.py


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'accounts.User'
