from django.db import models
from django.db.models import Q
from django.contrib.auth import get_user_model
from friendship.exceptions import FriendRequestAlreadyExists, FriendRequestDoesNotExist

User = get_user_model()
PENDING = 'pending'
ACCEPTED = 'accepted'
STATUS_CHOICES = {
    (PENDING, 'В ожидании'),
    (ACCEPTED, 'Принят'),
}
class Friendship(models.Model):

    from_user = models.ForeignKey(to=User, related_name='sender', on_delete=models.CASCADE)
    to_user = models.ForeignKey(to=User, related_name='receiver', on_delete=models.CASCADE)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default=PENDING)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['from_user', 'to_user'], name='unique_friendship')
        ]

    @staticmethod
    def get_friend_list(user):
        friends_list = Friendship.objects.filter(
            Q(from_user=user) | Q(to_user=user),
            status=ACCEPTED
        )
        return friends_list

    @staticmethod
    def add_friend_request(from_user, to_user):
        friendship, created = Friendship.objects.get_or_create(
            from_user=from_user,
            to_user=to_user,
            defaults={'status': Friendship.PENDING}  # Устанавливаем статус по умолчанию
        )
        if not created:
            raise FriendRequestAlreadyExists('Заявка в друзья уже отправлена.')
        return created

    @staticmethod
    def delete_friend_request(from_user, to_user):
        try:
            friend_request = Friendship.objects.get(
                from_user=from_user,
                to_user=to_user
            )
            friend_request.delete()
        except Friendship.DoesNotExist:
            raise FriendRequestDoesNotExist('Такой заявки в друзья не существует.')


