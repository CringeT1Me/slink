import logging

from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from friendship.models import Friendship

User = get_user_model()

logger = logging.getLogger(__name__)

class FriendshipPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Friendship
        fields = ['to_user', 'status']

    def validate_users(self, data):
        from_user = self.context['request'].user
        to_user = data.get('to_user')

        if from_user == to_user:
            raise ValidationError("Нельзя отправить запрос самому себе.")

        logger.debug(f'Отправитель: {from_user}, Получатель: {to_user}')

        return data

    def validate(self, data):
        return self.validate_users(data)


class FriendshipDeleteSerializer(FriendshipPostSerializer):
    decline = serializers.BooleanField()

    class Meta(FriendshipPostSerializer.Meta):
        fields = FriendshipPostSerializer.Meta.fields + ['decline']

    def validate(self, data):
        data = self.validate_users(data)

        decline = data.get('decline')
        if decline:
            data['from_user'], data['to_user'] = data['to_user'], self.context['request'].user

        return data