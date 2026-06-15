from .base import *

DEBUG = True
ALLOWED_HOSTS = ["*"]

MAIN_DOMAIN = "myapp.lvh.me:8000"
SESSION_COOKIE_DOMAIN = ".lvh.me"
CSRF_COOKIE_DOMAIN = ".lvh.me"
CSRF_TRUSTED_ORIGINS = [
    "http://*.lvh.me:8000",
    "http://lvh.me:8000",
]
