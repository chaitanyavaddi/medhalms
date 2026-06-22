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
    "ide",
    "jobs",
    "courses",
    "interviews",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "core.middleware.CacheableResponseMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
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
TIME_ZONE     = "UTC"
USE_I18N      = True
USE_TZ        = True

STATIC_URL       = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT      = BASE_DIR / "staticfiles"

AUTH_USER_MODEL = "users.User"
LOGIN_URL       = "/login/"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ── Site ──────────────────────────────────────────────────────────────
SITE_NAME = os.environ.get("SITE_NAME", "MedhaLMS")

# ── Background tasks ──────────────────────────────────────────────────
TASKS = {
    "default": {
        "BACKEND": "django.tasks.backends.immediate.ImmediateBackend",
    }
}

# ── Auth validation ───────────────────────────────────────────────────
NAME_LENGTH_RANGE     = (2,  50)   # (min, max)
PASSWORD_LENGTH_RANGE = (8, 128)   # (min, max)

# ── Google OAuth ──────────────────────────────────────────────────────
GOOGLE_CLIENT_ID     = os.environ.get("GOOGLE_CLIENT_ID", "")
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", "")

# ── File uploads ──────────────────────────────────────────────────────
DATA_UPLOAD_MAX_MEMORY_SIZE = 209715200   # 200 MB
FILE_UPLOAD_MAX_MEMORY_SIZE = 10485760    # 10 MB

# ── Bunny.net storage ─────────────────────────────────────────────────
BUNNY_STORAGE_ENDPOINT = os.environ.get("BUNNY_STORAGE_ENDPOINT", "https://sg.storage.bunnycdn.com")
BUNNY_STORAGE_ZONE     = os.environ.get("BUNNY_STORAGE_ZONE",     "your-zone")
BUNNY_ACCESS_KEY       = os.environ.get("BUNNY_ACCESS_KEY",       "")
BUNNY_CDN_BASE         = os.environ.get("BUNNY_CDN_BASE",         "https://cdn.myapp.com")

# ── Brand — 5 variables control the entire look and feel ─────────────
# Change these here; never hardcode colors in templates or CSS.
BRAND_DARK    = "#07111f"   # sidebar gradient top (darkest navy)
BRAND_NAVY    = "#0c2258"   # sidebar gradient mid
BRAND_BLUE    = "#1550be"   # primary blue — buttons, links, active states
BRAND_ACCENT  = "#e67f0f"   # orange accent — CTAs, highlights, active icons
BRAND_SURFACE = "#f5f2ee"   # warm cream — content area background

# Typography — IBM Plex Sans is loaded unconditionally in base.html.
# Override BRAND_FONT_FAMILY here if you swap fonts.
BRAND_FONT_URL    = ""
BRAND_FONT_FAMILY = "'IBM Plex Sans', 'Inter', system-ui, sans-serif"

# ── Third-party integrations ──────────────────────────────────────────
LOGO_DEV_TOKEN   = os.environ.get("LOGO_DEV_TOKEN", "")
JOBSPY_API_URL   = os.environ.get("JOBSPY_API_URL", "https://jobspy-production-76c6.up.railway.app")

# ── Email ─────────────────────────────────────────────────────────────
RESEND_API_KEY     = os.environ.get("RESEND_API_KEY", "")
EMAIL_FROM_NOREPLY = os.environ.get("EMAIL_FROM_NOREPLY", "App <noreply@myapp.com>")
EMAIL_FROM_UPDATES = os.environ.get("EMAIL_FROM_UPDATES", "App <updates@myapp.com>")
