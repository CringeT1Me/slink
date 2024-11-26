import logging

from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import GenericViewSet

from .exceptions import FriendRequestAlreadyExists
from .models import Friendship
from .serializers import FriendshipSerializer

logger = logging.getLogger(__name__)

class FriendshipView(GenericViewSet, CreateModelMixin, DestroyModelMixin):
    queryset = Friendship.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        return FriendshipSerializer

    def get_serializer(self, *args, **kwargs):
        kwargs['context'] = kwargs.get('context', {})
        kwargs['context']['request'] = self.request
        return super().get_serializer(*args, **kwargs)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        from_user = serializer.validated_data['from_user']
        to_user = serializer.validated_data['to_user']

        try:
            friendship = Friendship.add_friend_request(from_user, to_user)
            return Response(FriendshipSerializer(friendship).data,
                            status=status.HTTP_201_CREATED)
        except FriendRequestAlreadyExists as e:
            return Response({'status': 'error', 'message': str(e)},
                            status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        from_user = serializer.validated_data['from_user']
        to_user = serializer.validated_data['to_user']
        try:
            Friendship.delete_friend_request(from_user, to_user)
            return Response(serializer.data,
                            status=status.HTTP_200_OK)
        except FriendRequestAlreadyExists as e:
            return Response({'status': 'error', 'message': str(e)},
                            status=status.HTTP_400_BAD_REQUEST)

    @action(['POST'], detail=False, url_path='accept')
    def accept(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        from_user = serializer.validated_data['from_user']
        to_user = serializer.validated_data['to_user']
        try:
            friendship = Friendship.accept_friend_request(from_user, to_user)
            return Response(FriendshipSerializer(friendship).data,
                            status=status.HTTP_200_OK)
        except FriendRequestAlreadyExists as e:
            return Response({'status': 'error', 'message': str(e)},
                            status=status.HTTP_400_BAD_REQUEST)

    @action(['DELETE'], detail=False, url_path='decline')
    def decline(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        from_user = serializer.validated_data['from_user']
        to_user = serializer.validated_data['to_user']
        try:
            Friendship.decline_friend_request(from_user, to_user)
            return Response(serializer.data,
                            status=status.HTTP_200_OK)
        except FriendRequestAlreadyExists as e:
            return Response({'status': 'error', 'message': str(e)},
                            status=status.HTTP_400_BAD_REQUEST)