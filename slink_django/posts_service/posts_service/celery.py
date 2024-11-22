from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from kombu import Exchange, Queue
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'posts_service.settings')

app = Celery('posts_service')

app.config_from_object('django.conf:settings', namespace='CELERY')
album_exchange = Exchange('albums', type='direct')
album_init_queue = Queue('albums_init_queue', exchange=album_exchange, routing_key='albums.init')
album_add_avatar_queue = Queue('album_add_avatar_queue', exchange=album_exchange, routing_key='albums.add')
app.conf.task_queues = [album_init_queue, album_add_avatar_queue]

app.autodiscover_tasks()
