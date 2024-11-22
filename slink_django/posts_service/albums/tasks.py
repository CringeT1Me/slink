from albums.models import PostAlbum, AvatarAlbum, Image
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
        logger.info(f"Успешно созданы альбомы для пользователя {user_id}")
    except Exception as exc:
        error_text = f"Не удалось создать альбомы для пользователя {user_id}: {exc}"
        logger.error(error_text)
        return error_text
    return {'status': 'success', 'message': 'Альбомы успешно созданы'}

@app.task(bind=True, name='posts_service.albums_add_avatar', queue='albums_add_avatar_queue')
def albums_add_avatar(self, user_id, url):
    try:
        avatar_album = AvatarAlbum.objects.get(user_id=user_id)
        avatar = Image(user=user_id, url=url, album=avatar_album)
        avatar.save()
        logger.info(f"Успешно добавлен аватар {url} для пользователя {user_id}")
    except Exception as exc:
        error_text = f"Не удалось добавить аватар {url} для пользователя {user_id}: {exc}"
        logger.error(error_text)
        return error_text
    return {'status': 'success', 'message': 'Аватар успешно добавлен'}