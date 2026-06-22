import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent.parent.parent / '.env', override=False)

from .base import *

DEBUG = True

TASKS = {
    "default": {
        "BACKEND": "django.tasks.backends.dummy.DummyBackend",
    }
}
ALLOWED_HOSTS = ["*"]

MAIN_DOMAIN = "myapp.lvh.me:8000"
SESSION_COOKIE_DOMAIN = ".lvh.me"
CSRF_COOKIE_DOMAIN = ".lvh.me"
CSRF_TRUSTED_ORIGINS = [
    "http://*.lvh.me:8000",
    "http://lvh.me:8000",
]
