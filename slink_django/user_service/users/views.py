from gc import get_objects

from cities_light.models import Country, City
from djoser import signals
from djoser.compat import get_user_email
from djoser.conf import settings
from djoser.views import UserViewSet
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from users.models import User
from user_service.rabbitmq import receive_message
from users.serializers import CountrySerializer, CitySerializer, SendFriendRequestSerializer, \
    CancelFriendRequestSerializer, ProfileUserSerializer
from users.tasks import send_friend_request, cancel_friend_request


class CustomUserViewSet(UserViewSet):
    def get_serializer_class(self):
        if self.action == "create":
            if settings.USER_CREATE_PASSWORD_RETYPE:
                return settings.SERIALIZERS.user_create_password_retype
            return settings.SERIALIZERS.user_create
        elif self.action == "destroy" or (
            self.action == "me" and self.request and self.request.method == "DELETE"
        ):
            return settings.SERIALIZERS.user_delete
        elif self.action == "activation":
            return settings.SERIALIZERS.activation
        elif self.action == "resend_activation":
            return settings.SERIALIZERS.resend_activation
        elif self.action == "reset_password":
            return settings.SERIALIZERS.password_reset
        elif self.action == "reset_password_confirm":
            if settings.PASSWORD_RESET_CONFIRM_RETYPE:
                return settings.SERIALIZERS.password_reset_confirm_retype
            return settings.SERIALIZERS.password_reset_confirm
        elif self.action == "set_password":
            if settings.SET_PASSWORD_RETYPE:
                return settings.SERIALIZERS.set_password_retype
            return settings.SERIALIZERS.set_password
        elif self.action == "set_username":
            if settings.SET_USERNAME_RETYPE:
                return settings.SERIALIZERS.set_username_retype
            return settings.SERIALIZERS.set_username
        elif self.action == "reset_username":
            return settings.SERIALIZERS.username_reset
        elif self.action == "reset_username_confirm":
            if settings.USERNAME_RESET_CONFIRM_RETYPE:
                return settings.SERIALIZERS.username_reset_confirm_retype
            return settings.SERIALIZERS.username_reset_confirm
        elif self.action == "me":
            return settings.SERIALIZERS.current_user

        return self.serializer_class
    @action(["post"], detail=False)
    def activation(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.user
        user.is_verified = True
        user.is_active = True
        user.save()

        signals.user_activated.send(
            sender=self.__class__, user=user, request=self.request
        )

        if settings.SEND_CONFIRMATION_EMAIL:
            context = {"user": user}
            to = [get_user_email(user)]
            settings.EMAIL.confirmation(self.request, context).send(to)

        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(["post"], detail=False)
    def reset_password(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.get_user(serializer.validated_data)

        if user:
            context = {"user": user}
            to = [get_user_email(user)]
            settings.EMAIL.password_reset(self.request, context).send(to)

        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(["post"], detail=False, url_path=f"set_email")
    def set_email(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.request.user
        new_email = serializer.data["new_email"]
        if user:
            context = {"user": user}
            to = [new_email]
            settings.EMAIL.email_changed_confirmation(self.request, context).send(to)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(["post"], detail=False, url_path="set_email_confirm")
    def set_email_confirm(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Используем validated_data вместо data
        new_email = serializer.validated_data["new_email"]

        # Обновляем email пользователя
        serializer.user.email = new_email
        serializer.user.save()

        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(["GET"], detail=False, url_path=r'(?P<username>[^/.]+)')
    def retrieve_by_username(self, request, username=None):
        queryset = User.objects.all()
        user = get_object_or_404(queryset, username=username)
        serializer = ProfileUserSerializer(user)
        return Response(serializer.data)



class UsernameCheckView(APIView):
    def get(self, request, username):
        if User.objects.filter(username=username).exists():
            return Response({"available": False}, status=status.HTTP_200_OK)
        else:
            return Response({"available": True}, status=status.HTTP_200_OK)


class CountryListView(generics.ListAPIView):
    serializer_class = CountrySerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = Country.objects.all()
        query = self.request.query_params.get('q', None)
        if query:
            queryset = queryset.filter(name__icontains=query)
        return queryset

class CityListView(generics.ListAPIView):
    serializer_class = CitySerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = City.objects.all()
        country_id = self.request.query_params.get('country_id', None)
        query = self.request.query_params.get('q', None)
        if country_id:
            queryset = queryset.filter(country_id=country_id)
        if query:
            queryset = queryset.filter(search_names__icontains=query)
        return queryset

class SendFriendRequestView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = SendFriendRequestSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            from_user_id = serializer.validated_data['from_user_id']
            to_user_id = serializer.validated_data['to_user_id']
            response = send_friend_request(from_user_id, to_user_id)
            if response['status'] == 'success':
                return Response({'message': response['message']}, status=status.HTTP_200_OK)
            return Response({'message': response['message']}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CancelFriendRequestView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = CancelFriendRequestSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            from_user_id = serializer.validated_data['from_user_id']
            to_user_id = serializer.validated_data['to_user_id']
            response = cancel_friend_request(from_user_id, to_user_id)
            if response['status'] == 'success':
                return Response({'message': response['message']}, status=status.HTTP_200_OK)
            return Response({'message': response['message']}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeclineFriendRequestView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = SendFriendRequestSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            from_user_id = serializer.validated_data['from_user_id']
            to_user_id = serializer.validated_data['to_user_id']
            send_friend_request(from_user_id, to_user_id)
            response = receive_message('response_queue')
            if response['status'] == 'success':
                return Response({'message': response['message']}, status=status.HTTP_200_OK)
            return Response({'message': response['message']}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)