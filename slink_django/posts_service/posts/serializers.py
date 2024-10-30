from rest_framework import serializers

from albums.models import Image, PostAlbum
from posts.models import Post, PostImage

class PostImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(write_only=True)
    image_url = serializers.CharField(source='image.url', read_only=True)

    class Meta:
        model = PostImage
        fields = ['image', 'image_url']


class PostSerializer(serializers.ModelSerializer):
    images = serializers.ListField(
        child=serializers.ImageField(),
        write_only=True,
        required=False,
        max_length=10)
    post_images = PostImageSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'text', 'created_at', 'images', 'post_images']
