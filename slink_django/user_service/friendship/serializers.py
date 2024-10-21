from cities_light.models import Country, City
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.validators import validate_email
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.conf import settings
from djoser.serializers import UidAndTokenSerializer, UserCreateSerializer, SendEmailResetSerializer, \
    UserCreatePasswordRetypeSerializer
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.core import exceptions as django_exceptions
from rest_framework.settings import api_settings
import requests
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


User = get_user_model()

class SendFriendRequestSerializer(serializers.Serializer):
    to_user_username = serializers.CharField()

    def validate(self, attrs):
        to_user_username = attrs.get('to_user_username')
        from_user = self.context['request'].user
        try:
            to_user = User.objects.get(username=to_user_username)
        except User.DoesNotExist:
            raise serializers.ValidationError("Получатель запроса не существует.")

        if from_user == to_user:
            raise ValidationError("Нельзя отправить запрос самому себе.")

        attrs['from_user_id'] = from_user.id
        attrs['to_user_id'] = to_user.id

        return attrs

class CancelFriendRequestSerializer(SendFriendRequestSerializer):
    pass