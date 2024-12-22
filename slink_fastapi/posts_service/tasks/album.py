import logging
from core.celery_app import celery_app
from models.album import Album
from core.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

logger = logging.getLogger(__name__)

engine = create_engine(settings.database.sync_url, echo=True)
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)


@celery_app.task(bind=True, name="posts_service.albums_init", queue="albums_init_queue")
def albums_init(self, user_id):
    session = SessionLocal()
    try:
        post_album = Album.create_post_album(user_id=user_id)
        avatar_album = Album.create_avatar_album(user_id=user_id)

        session.add(post_album)
        session.add(avatar_album)

        session.commit()

        logger.info(f"Успешно созданы альбомы для пользователя {user_id}")
        return f"Успешно созданы альбомы для пользователя {user_id}"

    except Exception as exc:
        session.rollback()
        error_text = f"Не удалось создать альбомы для пользователя {user_id}: {exc}"
        logger.error(error_text)
        return error_text
    finally:
        session.close()
