from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
# Create your views here.

class PostViewSet(ModelViewSet):
    @action(methods=['GET'], path='ADasdasd')
    def get_posts:
