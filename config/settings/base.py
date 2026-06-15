import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = os.environ.get("SECRET_KEY", "django-insecure-local-dev-only-do-not-use-in-production")

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "template_partials",
    "users",
    "website",
    "authentication",
    "dashboard",
    "orgs",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "core.middleware.CacheableResponseMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "core.middleware.SubdomainMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "core.context_processors.brand",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

AUTH_USER_MODEL = "users.User"
LOGIN_URL = "/login/"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

MAIN_DOMAIN = "myapp.localhost:8000"

GOOGLE_CLIENT_ID     = os.environ.get("GOOGLE_CLIENT_ID", "")
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", "")

DATA_UPLOAD_MAX_MEMORY_SIZE = 209715200   # 200 MB — covers large video uploads
FILE_UPLOAD_MAX_MEMORY_SIZE = 10485760    # 10 MB — files above this go to temp disk

# ── Bunny.net storage ─────────────────────────────────────────────
BUNNY_STORAGE_ENDPOINT = os.environ.get("BUNNY_STORAGE_ENDPOINT", "https://sg.storage.bunnycdn.com")
BUNNY_STORAGE_ZONE     = os.environ.get("BUNNY_STORAGE_ZONE",     "your-zone")
BUNNY_ACCESS_KEY       = os.environ.get("BUNNY_ACCESS_KEY",       "")
BUNNY_CDN_BASE         = os.environ.get("BUNNY_CDN_BASE",         "https://cdn.myapp.com")

# ── Brand colours ────────────────────────────────────────────────────
BRAND_PRIMARY   = "#e67f0f"
BRAND_SECONDARY = "#f5f2ee"

# ── Brand fonts ──────────────────────────────────────────────────────
# Paste any Google Fonts (or other) URL here — it will be loaded in every page.
# BRAND_FONT_FAMILY must match the font-family name(s) in that URL.
BRAND_FONT_URL    = "https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap"
BRAND_FONT_FAMILY = "'Inter', system-ui, sans-serif"

CLOUDFLARE_API_TOKEN = os.environ.get('CLOUDFLARE_API_TOKEN', '')
CLOUDFLARE_ZONE_ID   = os.environ.get('CLOUDFLARE_ZONE_ID',   '')

RESEND_API_KEY      = os.environ.get('RESEND_API_KEY', '')
EMAIL_FROM_NOREPLY  = os.environ.get('EMAIL_FROM_NOREPLY', 'App <noreply@myapp.com>')
EMAIL_FROM_UPDATES  = os.environ.get('EMAIL_FROM_UPDATES',  'App <updates@myapp.com>')

RESERVED_SUBDOMAINS = [
    "dashboard", "billing", "contact", "me", "app", "api", "admin",
    "login", "logout", "signup", "register", "auth", "oauth",
    "account", "accounts", "profile", "settings", "config",
    "www", "mail", "email", "smtp", "pop", "imap", "ftp", "sftp",
    "ssh", "vpn", "cdn", "static", "assets", "media", "files",
    "ns", "ns1", "ns2", "dns", "mx", "ssl", "secure",
    "help", "support", "docs", "documentation", "status", "health",
    "news", "about", "jobs", "careers", "legal", "privacy",
    "terms", "press", "partners", "developers", "dev",
    "localhost", "test", "staging", "prod", "production", "demo",
    "beta", "alpha", "internal", "intranet", "portal", "myapp",
]
