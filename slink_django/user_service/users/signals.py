from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.conf import settings
from .models import User
import requests

from .tasks import create_albums


@receiver(post_save, sender=get_user_model())
def create_albums_signal(sender, instance, created, **kwargs):
    if created:
        response = create_albums(instance.id)
        print(response)


