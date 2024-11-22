from django.db import models

from albums.models import Image


# Create your models here.



class Post(models.Model):
    user = models.UUIDField()
    text = models.CharField(max_length=2000, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_archived = models.BooleanField(default=False)

class PostImage(models.Model):
    post = models.ForeignKey(to=Post, on_delete=models.CASCADE)
    image = models.ForeignKey(to=Image, on_delete=models.CASCADE)



