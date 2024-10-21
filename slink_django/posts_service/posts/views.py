from http.client import HTTPResponse

from django.shortcuts import render, get_object_or_404
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.permissions import IsAuthenticated

from posts.models import Post
from posts.serializers import PostSerializer


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, **kwargs):
        queryset = Post.objects.filter(is_archived=False)
        serializer = PostSerializer(queryset, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user.id)

    @action(methods=['POST'], detail=True, url_path='archive')
    def archive(self, request, pk=None):
        post = self.get_object()
        post.is_archived = True
        post.save()
        return Response(status=HTTP_200_OK, data={'message': 'Пост успешно архивирован.'})

    @action(methods=['POST'], detail=True, url_path='unarchive')
    def unarchive(self, request, pk=None):
        post = self.get_object()
        post.is_archived = False
        post.save()
        return Response(status=HTTP_200_OK, data={'message': 'Пост успешно разархивирован.'})

    @action(methods=['GET'], detail=False, url_path='archived')
    def list_archived(self, request):
        queryset = Post.objects.filter(is_archived=True)
        serializer = PostSerializer(queryset, many=True)
        return Response(serializer.data)

