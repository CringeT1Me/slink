from io import BytesIO
from PIL import Image

from files.storages import PublicAvatarStorage, PublicImageStorage
from files_service.celery import app

avatar_storage = PublicAvatarStorage()
image_storage = PublicImageStorage()

@app.task
def process_and_upload_avatar(file_data, file_name):
    try:
        # Открываем изображение
        image = Image.open(BytesIO(file_data))
        max_size = (300, 300)
        image.thumbnail(max_size, Image.Resampling.LANCZOS)

        # Сохраняем изображение в память
        thumb_io = BytesIO()
        image.save(thumb_io, format='JPEG', quality=80)
        thumb_io.seek(0)

        # Сохраняем файл в S3, используя MediaFileStorage
        avatar_storage.save(file_name, thumb_io)

        print(f"Image successfully uploaded to {file_name}")

    except Exception as e:
        print(f"Error processing and uploading avatar: {str(e)}")

@app.task
def process_and_upload_image(file_data, file_name):
    try:
        image = Image.open(BytesIO(file_data))
        max_size = (300, 300)
        image.thumbnail(max_size, Image.Resampling.LANCZOS)

        thumb_io = BytesIO()
        image.save(thumb_io, format='JPEG', quality=80)
        thumb_io.seek(0)

        image_storage.save(file_name, thumb_io)

        print(f"Изображение успешно загружено на {file_name}")

    except Exception as e:
        print(f"Ошибка обработки и загрузки изображения: {str(e)}")
