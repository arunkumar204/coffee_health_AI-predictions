import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'd0^(7m5tnx%dt+ky@(gv41l-oz=wtw8!oas+*)!jj@!s$-wgzw'
DEBUG = True

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'd0^(7m5tnx%dt+ky@(gv41l-oz=wtw8!oas+*)!jj@!s$-wgzw'
DEBUG = True

# ✅ FIXED: Correct ALLOWED_HOSTS format and dynamic configuration
ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    'coffee-health-ai-predictions.onrender.com',  # Without https://
]

# ✅ ADD: Dynamic host configuration for Render
RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

# -------------------------
# INSTALLED APPS
# -------------------------
INSTALLED_APPS = [
    # Default Django apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-party apps
    'rest_framework',
    'corsheaders',

    # Allauth apps
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',

    # Local apps
    'api',
]

# Required by Allauth
SITE_ID = 1

# -------------------------
# MIDDLEWARE
# -------------------------
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',

    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',

    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',

    # Allauth required middleware (must be after AuthenticationMiddleware)
    'allauth.account.middleware.AccountMiddleware',

    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# -------------------------
# URLS & TEMPLATES
# -------------------------
ROOT_URLCONF = 'coffee_health.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'coffee_health' / 'templates'
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

# -------------------------
# STATIC FILES
# -------------------------
STATIC_URL = 'static/'
STATICFILES_DIRS = [
    BASE_DIR / 'coffee_health' / 'static'
]

# -------------------------
# WSGI APPLICATION
# -------------------------
WSGI_APPLICATION = 'coffee_health.wsgi.application'

# -------------------------
# DATABASE
# -------------------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# -------------------------
# CORS SETTINGS
# -------------------------
CORS_ALLOW_ALL_ORIGINS = True

# -------------------------
# REST FRAMEWORK AUTH
# -------------------------
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}

