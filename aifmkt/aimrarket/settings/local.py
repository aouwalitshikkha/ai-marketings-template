from .base import *

DEBUG = True

SECRET_KEY = 'django-insecure-r(b-+%)nm@_8!#)s%*$15b00w1oo))!jkyt-jwsph3$o2t(8j_'

ALLOWED_HOSTS = []

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
        'CONN_MAX_AGE': 60,
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'django_cache',
    }
}
