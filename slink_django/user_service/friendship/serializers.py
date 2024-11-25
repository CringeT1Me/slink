import logging

from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from friendship.models import Friendship

User = get_user_model()

logger = logging.getLogger(__name__)

class FriendshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Friendship
        fields = ['from_user', 'to_user', 'status']
        read_only_fields = ['from_user', 'status']

    def validate_users(self, data):
        from_user = self.context['request'].user
        to_user = data.get('to_user')

        if from_user == to_user:
            raise ValidationError("Нельзя отправить запрос самому себе.")

        logger.debug(f'Отправитель: {from_user}, Получатель: {to_user}')

        data['from_user'] = from_user
        return data

    def validate(self, data):
        return self.validate_users(data)