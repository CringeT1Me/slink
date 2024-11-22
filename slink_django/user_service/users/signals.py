from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.conf import settings

from user_service.celery import app
from .models import User
import requests



@receiver(post_save, sender=get_user_model())
def create_albums_signal(sender, instance, created, **kwargs):
    if created:
        response = app.send_task('posts_service.albums_init',
                                 args=[instance.id],
                                 exchange='albums',
                                 routing_key='albums.init'
                                 )
        print(response.get(timeout=15))


