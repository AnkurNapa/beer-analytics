"""
Beer Analytics Django settings — PostgreSQL + minimal config
"""
import os
from pathlib import Path
import environ

BASE_DIR = Path(__file__).resolve().parent.parent
env = environ.Env(DEBUG=(bool, False))
environ.Env.read_env(BASE_DIR / ".env")

SECRET_KEY = env("SECRET_KEY")
DEBUG = env("DEBUG")
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["*"])

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",
    "meta",
    "recipe_db",
    "web_app",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "web_app.context_processors.unit_system",
            ],
        },
    },
]

# PostgreSQL Database
DATABASES = {
    "default": env.db("DATABASE_URL")
}

# Auto-field
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Database cache (survives Railway restarts unlike FileBasedCache)
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.db.DatabaseCache",
        "LOCATION": "cache_table",
        "TIMEOUT": env.int("PAGE_CACHE_SECONDS", default=3600),
    },
    "data": {
        "BACKEND": "django.core.cache.backends.db.DatabaseCache",
        "LOCATION": "cache_table_data",
        "TIMEOUT": env.int("DATA_CACHE_SECONDS", default=86400),
    },
}

DEFAULT_PAGE_CACHE_TIME = env.int("PAGE_CACHE_SECONDS", default=3600)

# Static files
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Sessions (for metric unit preference)
SESSION_ENGINE = "django.contrib.sessions.backends.db"
SESSION_COOKIE_AGE = 60 * 60 * 24 * 365  # 1 year

# Internationalization
TIME_ZONE = env("TIME_ZONE", default="Asia/Kolkata")
USE_TZ = True
USE_I18N = True
LANGUAGE_CODE = "en-us"
USE_THOUSAND_SEPARATOR = True

# django-meta
META_SITE_PROTOCOL = "https" if not DEBUG else "http"
META_USE_OG_PROPERTIES = True
META_USE_TWITTER_PROPERTIES = True

# Security (when DEBUG=False)
if not DEBUG:
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 2628000
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    SECURE_SSL_REDIRECT = True
