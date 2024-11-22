from .base import *

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('POSTGRES_TEST_NAME'),
        'USER': os.environ.get('POSTGRES_TEST_USER'),
        'PASSWORD': os.environ.get('POSTGRES_TEST_PASSWORD'),
        'HOST': os.environ.get('POSTGRES_TEST_HOST'),
        'PORT': 5432,
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