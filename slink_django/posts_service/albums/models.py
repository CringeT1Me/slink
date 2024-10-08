from django.db import models

# Create your models here.
class Album(models.Model):
    user = models.UUIDField()
    name = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'name']


class PostAlbum(Album):
    name = models.CharField(max_length=30, default='Посты', editable=False)

    class Meta:
        proxy = True


class AvatarAlbum(Album):
    name = models.CharField(max_length=30, default='Аватарки', editable=False)

    class Meta:
        proxy = True


class Image(models.Model):
    user = models.UUIDField()
    album = models.ForeignKey(to=Album, on_delete=models.CASCADE)
    url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)