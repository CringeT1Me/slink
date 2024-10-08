import uuid
from io import BytesIO

import boto3
from PIL import Image
from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from files.serializers import FileUploadSerializer
from files.storages import PublicAvatarStorage
from files.tasks import process_and_upload_avatar


class UploadAvatar(APIView):
    def post(self, request, *args, **kwargs):
        if 'file' not in request.FILES:
            return JsonResponse({'error': 'Файл не обнаружен'}, status=400)
        file = request.FILES['file']
        if not file.name.lower().endswith(('.jpg', '.jpeg', '.png')):
            file.name = f"{file.name}.jpg"
        # Генерация уникального имени файла
        unique_file_name = f"{uuid.uuid4()}_{file.name}"

        try:
            # Запуск задачи на обработку и загрузку файла через Celery
            process_and_upload_avatar.delay(file.read(), unique_file_name)

            # Формирование ссылки на аватар
            avatar_url = f"{settings.AWS_S3_ENDPOINT_URL}/{settings.AWS_STORAGE_BUCKET_NAME}/{PublicAvatarStorage.location}/{unique_file_name}"

            return JsonResponse({'url': avatar_url}, status=200)

        except Exception as e:
            return JsonResponse({'error': f'Failed to upload file: {str(e)}'}, status=500)