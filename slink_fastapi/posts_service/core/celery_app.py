from __future__ import absolute_import, unicode_literals
from celery import Celery
from kombu import Exchange, Queue
from core.config import settings, CelerySettings

celery: CelerySettings = CelerySettings()

celery_app = Celery(
    "posts_service",
    broker=celery.broker_url,
    backend=celery.result_backend,
)

celery_app.conf.update(
    task_routes={
        "posts_service.albums_init": {"queue": "albums_init_queue"},
        "posts_service.albums_add_avatar": {"queue": "albums_add_avatar_queue"},
    }
)

album_exchange = Exchange("albums", type="direct")
album_init_queue = Queue(
    "albums_init_queue", exchange=album_exchange, routing_key="albums.init"
)
album_add_avatar_queue = Queue(
    "album_add_avatar_queue", exchange=album_exchange, routing_key="albums.add"
)
celery_app.conf.task_queues = [album_init_queue, album_add_avatar_queue]

celery_app.autodiscover_tasks()
