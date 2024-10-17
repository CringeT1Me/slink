from logging import exception
from albums.models import PostAlbum, AvatarAlbum
from posts_service.celery import app
import logging

logger = logging.getLogger(__name__)

@app.task(bind=True)  # bind=True позволяет захватить саму задачу для обработки ошибок
def create_albums(self, message):
    user_id = message['user_id']
    try:
        # Создаем два альбома для пользователя
        post_album = PostAlbum(user=user_id)
        avatar_album = AvatarAlbum(user=user_id)
        post_album.save()
        avatar_album.save()
        logger.info(f"Successfully created albums for user {user_id}")
    except Exception as exc:
        logger.error(f"Failed to create albums for user {user_id}: {exc}")
        raise self.retry(exc=exc, countdown=60, max_retries=3)  # Попытки повторного выполнения задачи
    return {'status': 'success', 'message': 'Альбомы успешно созданы'}
