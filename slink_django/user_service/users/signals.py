from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

from user_service.celery import app



@receiver(post_save, sender=get_user_model())
def create_albums_signal(sender, instance, created, **kwargs):
    if created:
        try:
            response = app.send_task('posts_service.albums_init',
                                     args=[instance.id],
                                     exchange='albums',
                                     routing_key='albums.init'
                                     )
            print(response.get(timeout=1))
        except Exception:
            print("Не удалось создать альбомы для пользователя в post_service")



