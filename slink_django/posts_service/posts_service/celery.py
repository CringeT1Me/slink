from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from kombu import Exchange, Queue
# Устанавливаем настройки Django для Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'posts_service.settings')

app = Celery('posts_service')

# Загружаем настройки из конфигурации Django с префиксом 'CELERY_'
app.config_from_object('django.conf:settings', namespace='CELERY')
album_exchange = Exchange('albums', type='direct')
album_queue = Queue('albums_init_queue', exchange=album_exchange, routing_key='albums.init')
# Автоматически находит задачи в зарегистрированных приложениях Django
app.conf.task_queues = [album_queue]


app.autodiscover_tasks()
