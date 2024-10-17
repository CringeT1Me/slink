from http.client import HTTPResponse

from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.permissions import IsAuthenticated

from albums.models import Album
from posts.models import Post
from posts.serializers import PostSerializer


# Create your views here.

class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Передаем user_id из токена
        serializer.save(user=self.request.user.id)

    @action(methods=['POST'], detail=True, url_path=r'(?P<id>\d+)/archive/')
    def archive(self, request, pk=None):
        post = self.get_object()
        post.is_archived = True
        post.save()
        return Response(status=HTTP_200_OK, data={'message': 'Пост успешно архивирован'})
