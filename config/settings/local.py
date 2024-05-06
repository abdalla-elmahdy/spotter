from .base import *

# These settings should only be used for development only
# NOT SUITABLE FOR PRODUCTION

SECRET_KEY = "thisisinsecureandonlyforlocaldev"

DEBUG = True

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"


# Database
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# Static files handling
STATIC_URL = "static/"