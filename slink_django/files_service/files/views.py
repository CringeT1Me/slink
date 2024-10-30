import uuid

from django.conf import settings
from django.http import JsonResponse
from rest_framework.views import APIView

from files.storages import PublicAvatarStorage, PublicImageStorage
from files.tasks import process_and_upload_avatar, process_and_upload_image


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

class UploadImages(APIView):
    def post(self, request, *args, **kwargs):
        files = request.FILES.getlist('files')
        if not files:
            return JsonResponse({'error': 'Файлы не обнаружены'}, status=400)
        image_urls = []
        for file in files:
            if not file.name.lower().endswith(('.jpg', '.jpeg', '.png')):
                file.name = f"{files.name}.jpg"
            unique_file_name = f"{uuid.uuid4()}_{file.name}"

            try:
                process_and_upload_image.delay(file.read(), unique_file_name)

                avatar_url = f"{settings.AWS_S3_ENDPOINT_URL}/{settings.AWS_STORAGE_BUCKET_NAME}/{PublicImageStorage.location}/{unique_file_name}"

                image_urls.append(avatar_url)

            except Exception as e:
                return JsonResponse({'error': f'Не удалось загрузить изображение: {str(e)}'}, status=500)

        return JsonResponse({'urls': image_urls}, status=200)