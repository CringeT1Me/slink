import logging
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .exceptions import FriendRequestAlreadyExists, FriendRequestDoesNotExist
from .models import Friendship, ACCEPTED
from .serializers import FriendshipPostSerializer, FriendshipDeleteSerializer

logger = logging.getLogger(__name__)

class FriendshipView(GenericAPIView, CreateModelMixin, DestroyModelMixin):
    queryset = Friendship.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return FriendshipPostSerializer
        elif self.request.method == 'DELETE':
            return FriendshipDeleteSerializer
        return super().get_serializer_class()

    def get_serializer(self, *args, **kwargs):
        kwargs['context'] = kwargs.get('context', {})
        kwargs['context']['request'] = self.request
        return super().get_serializer(*args, **kwargs)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        from_user_id = serializer.validated_data['from_user'].id
        to_user_id = serializer.validated_data['to_user'].id

        try:
            Friendship.objects.add_friend_request(from_user_id, to_user_id)
            return Response({'status': 'success', 'message': 'Заявка в друзья успешно отправлена.'},
                            status=status.HTTP_201_CREATED)
        except FriendRequestAlreadyExists as e:
            return Response({'status': 'error', 'message': str(e)},
                            status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        from_user_id = serializer.validated_data['from_user'].id
        to_user_id = serializer.validated_data['to_user'].id

        try:
            Friendship.objects.delete_friend_request(from_user_id, to_user_id)
            return Response({'status': 'success', 'message': 'Заявка в друзья отменена.'}, status=status.HTTP_200_OK)
        except FriendRequestDoesNotExist as e:
            return Response({'status': 'error', 'message': str(e)}, status=status.HTTP_404_NOT_FOUND)