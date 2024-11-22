from django.db import models

# Create your models here.

class Chat(models.Model):
    users = models.JSONField()
    is_group = models.BooleanField()

class Message(models.Model):
    user = models.UUIDField()
    chat = models.ForeignKey(to=Chat, on_delete=models.CASCADE)
    text = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_edited = models.BooleanField(default=False)
    edited_at = models.DateTimeField(auto_now=True, null=True, blank=True)

class MessageImage(models.Model):
    message = models.ForeignKey(to=Message, on_delete=models.CASCADE)
    image = models.URLField()



