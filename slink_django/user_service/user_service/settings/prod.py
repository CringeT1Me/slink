from .base import *

DEBUG = False
ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'user_service']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('POSTGRES_USERS_NAME'),
        'USER': os.environ.get('POSTGRES_USERS_USER'),
        'PASSWORD': os.environ.get('POSTGRES_USERS_PASSWORD'),
        'HOST': os.environ.get('POSTGRES_USERS_HOST'),
        'PORT': 5432,
    }
}