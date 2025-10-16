import os
from pathlib import Path

# 🔹 Base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# 🔹 SECURITY
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "change-me-in-production")
DEBUG = os.environ.get("DEBUG", "True") == "True"
ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "*").split(",")

# 🔹 Installed apps
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "corsheaders",
    'rest_framework',
    'rest_framework.authtoken',
    # Add your apps here, e.g., 'api', 'frontend'
    'tracker',  # <-- your new app
]

# JWT Auth
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}


# 🔹 Middleware
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # 👈 add this at the top (right after SecurityMiddleware ideally)
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'backend.urls'

# 🔹 Templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],  # Optional, for custom templates
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

# 🔹 Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get("POSTGRES_DB", "devdb"),
        'USER': os.environ.get("POSTGRES_USER", "devuser"),
        'PASSWORD': os.environ.get("POSTGRES_PASSWORD", "devpass"),
        'HOST': os.environ.get("POSTGRES_HOST", "postgres"),
        'PORT': 5432,
    }
}

AUTH_USER_MODEL = 'tracker.User'

# 🔹 Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# 🔹 Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# 🔹 Static files
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'  # Django collects static here

# Optional: Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# 🔹 Default primary key
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Allow your frontend origin
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://192.168.50.113:5173",
]

# Optional: allow all (for dev only!)
# CORS_ALLOW_ALL_ORIGINS = True
