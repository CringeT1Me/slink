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

class ProfileUserSerializer(serializers.ModelSerializer):
    country_name = serializers.SerializerMethodField()
    city_name = serializers.SerializerMethodField()
    # Поле для записи (прием файла)
    avatar_file = serializers.ImageField(write_only=True, required=False)

    class Meta:
        model = User
        fields = [
            'username', 'first_name', 'last_name', 'email', 'phone', 'description',
            'is_active', 'city', 'city_name', 'country', 'country_name', 'avatar_url', 'avatar_file'
        ]

    def get_user(self, attrs):
        username = attrs.get("username")
        try:
            # Ищем пользователя по username, email или phone
            user = User.objects.get(
                Q(username__iexact=username) |
                Q(email__iexact=username) |
                Q(phone__iexact=username)
            )
        except User.DoesNotExist:
            raise serializers.ValidationError({"username": "Пользователь с такими данными не найден."})

        # Сохраняем найденного пользователя для дальнейшего использования
        self.user = user
        return user

    def get_country_name(self, obj):
        # Проверяем, есть ли у пользователя страна
        if obj.country:
            return obj.country.name  # Возвращаем название страны
        return None  # Если страна не указана, возвращаем None

    def get_city_name(self, obj):
        # Проверяем, есть ли у пользователя город
        if obj.city:
            return obj.city.name  # Возвращаем название города
        return None  # Если город не указан, возвращаем None

    def update(self, instance, validated_data):
        # Обрабатываем загрузку аватара, если он есть
        avatar_file = validated_data.pop('avatar_file', None)

        if avatar_file:
            # Здесь вызывайте логику отправки на files_service и получите URL
            files_service_url = f"{settings.FILES_SERVICE_URL}/api/v1/upload-avatar/"
            files = {'file': avatar_file}
            response = requests.post(files_service_url, files=files)

            if response.status_code == 200:
                avatar_url = response.json().get('url')
                print('bugagashke')
                instance.avatar_url = avatar_url
            else:
                raise serializers.ValidationError("Failed to upload avatar to the files service.")

        # Остальные данные обновляем стандартно
        return super().update(instance, validated_data)


class CustomSendEmailResetSerializer(serializers.Serializer):
    username = serializers.CharField()

    def get_user(self, attrs):
        username = attrs.get("username")
        try:
            # Ищем пользователя по username, email или phone
            user = User.objects.get(
                Q(username__iexact=username) |
                Q(email__iexact=username) |
                Q(phone__iexact=username)
            )
        except User.DoesNotExist:
            raise serializers.ValidationError({"username": "Пользователь с такими данными не найден."})

        # Сохраняем найденного пользователя для дальнейшего использования
        self.user = user
        return user



class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'first_name', 'last_name')

    def validate(self, attrs):
        user = User(**attrs)
        password = attrs.get("password")
        email = attrs.get('email')
        try:
            validate_password(password, user)
        except django_exceptions.ValidationError as e:
            serializer_error = serializers.as_serializer_error(e)
            raise serializers.ValidationError(
                {"password": serializer_error[api_settings.NON_FIELD_ERRORS_KEY]}
            )
        try:
            validate_email(email)
        except django_exceptions.ValidationError:
            raise serializers.ValidationError(
                {'email': 'Данная почта не существует'}
            )
        if User.objects.filter(email__iexact=email).exists():
            raise serializers.ValidationError(
                {'email': "Данная почта уже используется."}
            )
        return attrs


class SetEmailSerializer(serializers.Serializer):
    new_email = serializers.EmailField()

    def validate_new_email(self, new_email):
        from django.core.validators import validate_email
        validate_email(new_email)
        if User.objects.filter(email__iexact=new_email).exists():
            raise serializers.ValidationError(
                {'email': 'Данная почта уже используется'}
            )
        return new_email

class SetEmailConfirmSerializer(UidAndTokenSerializer):
    encoded_new_email = serializers.CharField()

    def validate(self, attrs):
        attrs = super().validate(attrs)
        try:
            new_email = force_str(urlsafe_base64_decode(attrs.get("encoded_new_email", "")))
            validate_email(new_email)
            if User.objects.filter(email__iexact=new_email).exists():
                raise serializers.ValidationError("Данная почта уже используется.")
            attrs['new_email'] = new_email
        except (User.DoesNotExist, ValueError, TypeError, OverflowError):
            key_error = "invalid_email"
            raise serializers.ValidationError(
                {"new_email": [self.error_messages.get(key_error, "Invalid email.")]}, code=key_error
            )
        return attrs


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['id', 'name']

class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['id', 'display_name', 'country']

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


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['user_role'] = user.role

        return token