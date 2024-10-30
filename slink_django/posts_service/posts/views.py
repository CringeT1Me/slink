from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers
from django.conf import settings
import requests

from albums.models import Image
from posts.models import Post, PostImage
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
        post = serializer.save(user=self.request.user.id)
        images_data = self.request.data.getlist('images', [])

        if images_data:
            files_service_url = f"{settings.FILES_SERVICE_URL}/api/v1/upload-images/"
            files = [('files', img) for img in images_data]
            response = requests.post(files_service_url, files=files)

            if response.status_code == 200:
                image_urls = response.json().get('urls', [])
                images = [Image(user=post.user, url=url) for url in image_urls]
                Image.objects.bulk_create(images)
                post_images = [PostImage(post=post, image=image) for image in images]
                PostImage.objects.bulk_create(post_images)
            else:
                raise serializers.ValidationError("Не удалось загрузить изображения в files_service.")

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

