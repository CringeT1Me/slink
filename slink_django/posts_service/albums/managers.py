from django.db import models

class AvatarAlbumManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(name='Аватарки')

    def get(self, user_id):
        return self.get_queryset().get(user=user_id)

class PostAlbumManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(name='Посты')

    def get(self, user_id):
        return self.get_queryset().get(user=user_id)