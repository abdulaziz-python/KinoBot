import os

# Database Cache Configuration
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.db.DatabaseCache",
        "LOCATION": "django_cache",
    }
}

# Cache Middleware Timeout (ensure it's an integer)
CACHE_MIDDLEWARE_SECONDS = int(os.getenv("CACHE_TIMEOUT", 300))

# Session engine based on database
SESSION_ENGINE = "django.contrib.sessions.backends.db"
SESSION_CACHE_ALIAS = "default"
