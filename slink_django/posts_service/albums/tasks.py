from logging import exception
from albums.models import PostAlbum, AvatarAlbum
from posts_service.celery import app
import logging

logger = logging.getLogger(__name__)

@app.task(bind=True, name='posts_service.albums_init', queue='albums_init_queue')  # bind=True позволяет захватить саму задачу для обработки ошибок
def albums_init(self, user_id):
    try:
        post_album = PostAlbum(user=user_id)
        avatar_album = AvatarAlbum(user=user_id)
        post_album.save()
        avatar_album.save()
        print('работает!!!!!')
        logger.info(f"Successfully created albums for user {user_id}")
    except Exception as exc:
        error_text = f"Failed to create albums for user {user_id}: {exc}"
        logger.error(error_text)
        return error_text
    return {'status': 'success', 'message': 'Альбомы успешно созданы'}
