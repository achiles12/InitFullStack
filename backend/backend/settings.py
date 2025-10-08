# backend/backend/settings.py
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Static files
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
# Static files (CSS, JavaScript, Images)
# STATIC_URL = '/static/'
# Optional: for local dev, serve them from a folder
# STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')


SECRET_KEY = 'replace-this-with-a-real-secret-key'
DEBUG = True
ALLOWED_HOSTS = ['*']  # For Docker/local development

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Add your custom apps here, e.g.:
    # 'myapp',
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

ROOT_URLCONF = 'backend.urls'  # ✅ <--- This tells Django where your main urls.py lives


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

WSGI_APPLICATION = 'backend.wsgi.application'

# Database, etc...

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "devdb",
        "USER": "devuser",
        "PASSWORD": "devpass",
        "HOST": "postgres",  # must match service name in docker-compose
        "PORT": "5432",
    }
}

