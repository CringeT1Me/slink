from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import FriendRequestAlreadyExists, Friendship
from .serializers import SendFriendRequestSerializer


class SendFriendRequestView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = SendFriendRequestSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            try:
                Friendship.add_friend_request(from_user_id, to_user_id)
                return Response({'status': 'success', 'message': 'Заявка в друзья успешно отправлена.'},
                                status=status.HTTP_201_CREATED)
            except FriendRequestAlreadyExists as e:
                return Response({'status': 'error', 'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
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