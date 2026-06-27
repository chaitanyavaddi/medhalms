import os
from .base import *

DEBUG = False

ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "myapp.com").split(",")

MAIN_DOMAIN = os.environ.get("MAIN_DOMAIN", "myapp.com")

# Cookies scoped to root domain so subdomain sessions work
SESSION_COOKIE_DOMAIN = os.environ.get("SESSION_COOKIE_DOMAIN", ".myapp.com")
CSRF_COOKIE_DOMAIN    = os.environ.get("CSRF_COOKIE_DOMAIN",    ".myapp.com")
CSRF_TRUSTED_ORIGINS  = os.environ.get("CSRF_TRUSTED_ORIGINS", "https://*.myapp.com,https://myapp.com").split(",")

# HTTPS
SECURE_PROXY_SSL_HEADER      = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_SSL_REDIRECT           = True
SESSION_COOKIE_SECURE         = True
CSRF_COOKIE_SECURE            = True
SECURE_HSTS_SECONDS           = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD           = True

# Allow Puter auth popup to communicate back via window.opener
SECURE_CROSS_ORIGIN_OPENER_POLICY = "same-origin-allow-popups"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("DB_NAME", "postgres"),
        "USER": os.environ.get("DB_USER", ""),
        "PASSWORD": os.environ.get("DB_PASSWORD", ""),
        "HOST": os.environ.get("DB_HOST", ""),
        "PORT": os.environ.get("DB_PORT", "5432"),
        "OPTIONS": {
            "sslmode": os.environ.get("DB_SSLMODE", "require"),
        },
        "CONN_MAX_AGE": 600,
        "CONN_HEALTH_CHECKS": True,
    }
}

# Static files served by WhiteNoise
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}
