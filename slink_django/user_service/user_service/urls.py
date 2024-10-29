from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import SimpleRouter

from friendship.views import FriendshipView
from users.views import UsernameCheckView, CustomUserViewSet, CountryListView, CityListView

router = SimpleRouter()
router.register(r'api/v1/users', CustomUserViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/countries/', CountryListView.as_view(), name='country-list'),
    path('api/v1/cities/', CityListView.as_view(), name='city-list'),
    path('api/v1/check-username/<str:username>/', UsernameCheckView.as_view(), name='check-username'),
    path('api/v1/users/', include('djoser.urls.jwt')),
    path('api/v1/friendship/', FriendshipView.as_view(), name='friendship')
]

urlpatterns += router.urls