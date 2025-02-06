import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-++2)6&l^g*sjq&79hwk(o6#--92hmv(y1jsxul9t^=z0a@+$5l'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'trips',
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

ROOT_URLCONF = 'wycieczkomat.urls'

# Konfiguracja plików statycznych
STATIC_URL = '/static/'

STATICFILES_DIRS = [
    BASE_DIR / "wycieczkomat/static",  # Upewnij się, że masz właściwy katalog
]

# Katalog, do którego Django zbierze wszystkie pliki statyczne po użyciu collectstatic
STATIC_ROOT = BASE_DIR / "staticfiles"

# Konfiguracja szablonów
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "wycieczkomat/templates"],  # Katalog z szablonami
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

WSGI_APPLICATION = 'wycieczkomat.wsgi.application'

# Konfiguracja bazy danych - PostgreSQL
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('POSTGRES_DB') or 'wycieczkomat',
        'USER': os.environ.get('POSTGRES_USER') or 'postgres',
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD') or 'postgres',
        'HOST': os.environ.get('POSTGRES_HOST') or 'db',
        'PORT': os.environ.get('POSTGRES_PORT') or '5433',
    }
}

# Password validation
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
LANGUAGE_CODE = 'pl-PL'
TIME_ZONE = 'Europe/Warsaw'
USE_I18N = True
USE_TZ = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Konfiguracja wysyłania e-maili przy użyciu SMTP Brevo
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'wycieczkomat@gmail.com'       # Twój adres Gmail
EMAIL_HOST_PASSWORD = 'oeygdxtivwexdtda'  # Hasło do aplikacji lub Twoje hasło (patrz uwagi poniżej)
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
