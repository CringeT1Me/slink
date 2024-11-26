from django.urls import path, include
from django.views.decorators.cache import cache_page
from rest_framework.routers import SimpleRouter

from users.views import CustomUserViewSet, UsernameCheckView

router = SimpleRouter()
router.register(r'api/v1/users', CustomUserViewSet, basename='user')


users_urlpatterns = [
    path('api/v1/check-username/<str:username>/', cache_page(60 * 15)(UsernameCheckView.as_view()), name='check-username'),
    path('api/v1/users/', include('djoser.urls.jwt')),
]

users_urlpatterns += router.urls