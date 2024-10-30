from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from albums.models import Album
from albums.serializers import AlbumSerializer


class AlbumViewSet(ModelViewSet):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer
