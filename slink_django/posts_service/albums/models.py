from django.db import models

# Create your models here.
class Album(models.Model):
    user = models.UUIDField()
    name = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'name']


class PostAlbum(Album):
    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        self.name = 'Посты'
        super().save(*args, **kwargs)


class AvatarAlbum(Album):
    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        self.name = 'Аватарки'
        super().save(*args, **kwargs)


class Image(models.Model):
    user = models.UUIDField()
    album = models.ForeignKey(to=Album, on_delete=models.CASCADE)
    url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)