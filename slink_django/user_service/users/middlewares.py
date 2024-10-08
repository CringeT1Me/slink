from django.conf import settings
from django.utils.timezone import now
from datetime import timedelta
from django.urls import resolve

class UpdateLastOnlineMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Разрешаем middleware работать только для GET запросов
        if request.method == 'GET':
            resolver_match = resolve(request.path)
            current_view = resolver_match.func.__name__
            current_view_class = resolver_match.func.view_class if hasattr(resolver_match.func, 'view_class') else None

            # Проверка исключённых путей
            if request.path in getattr(settings, 'LAST_ONLINE_EXCLUDED_PATHS', []):
                return self.get_response(request)

            # Проверка исключённых представлений по имени
            if current_view in getattr(settings, 'LAST_ONLINE_EXCLUDED_VIEWS', []):
                return self.get_response(request)

            # Проверка исключённых классов представлений
            if current_view_class in getattr(settings, 'LAST_ONLINE_EXCLUDED_VIEW_CLASSES', []):
                return self.get_response(request)

            # Если ни одно из условий исключения не выполнено, обновляем last_online
            if request.user.is_authenticated:
                now_time = now()
                if request.user.last_online is None or now_time - request.user.last_online > timedelta(minutes=5):
                    request.user.last_online = now_time
                    request.user.save(update_fields=['last_online'])

        return self.get_response(request)