from .base import *

DEBUG = True

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

DJOSER_EMAIL = {
    'activation': 'users.emails.TestActivationEmail'
}

if 'EMAIL' in DJOSER:
    DJOSER['EMAIL'].update(DJOSER_EMAIL)
else:
    DJOSER['EMAIL'] = DJOSER_EMAIL

