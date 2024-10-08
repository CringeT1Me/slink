from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Устанавливаем настройки Django для Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'friendship_service.settings')

app = Celery('friendship_service')

# Загружаем настройки из конфигурации Django с префиксом 'CELERY_'
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматически находит задачи в зарегистрированных приложениях Django
app.autodiscover_tasks()
