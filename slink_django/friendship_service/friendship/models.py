from django.db import models

# Create your models here.

class Friendship(models.Model):
    PENDING = 'pending'
    ACCEPTED = 'accepted'
    STATUS_CHOICES = {
        (PENDING, 'В ожидании'),
        (ACCEPTED, 'Принят'),
    }
    from_user_id = models.UUIDField()  # or IntegerField depending on your user model's primary key
    to_user_id = models.UUIDField()
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default=PENDING)  # e.g., pending, accepted, declined
    # created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('from_user_id', 'to_user_id')

    @staticmethod
    def add_friend_request(from_user_id, to_user_id):
        friendship, created = Friendship.objects.get_or_create(
            from_user_id=from_user_id,
            to_user_id=to_user_id,
            defaults={'status': Friendship.PENDING}  # Устанавливаем статус по умолчанию
        )
        if created:
            return {'status': 'success', 'message' :'Заявка в друзья успешно отправлена.'}
        else:
            return {'status': 'error', 'message' :'Заявка в друзья уже отправлена.'}

    @staticmethod
    def delete_friend_request(from_user_id, to_user_id):
        friend_request = Friendship.objects.get(
            from_user_id=from_user_id,
            to_user_id=to_user_id,
            defaults={'status': Friendship.PENDING}  # Устанавливаем статус по умолчанию
        )
        if friend_request:
            friend_request.delete()
            return {'status': 'success', 'message' :'Заявка в друзья отменена.'}
        else:
            return {'status': 'error', 'message' :'Такой заявки в друзья не существует.'}