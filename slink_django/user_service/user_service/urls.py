import debug_toolbar
from django.contrib import admin
from django.urls import path, include
from django.views.decorators.cache import cache_page
from rest_framework.routers import SimpleRouter

from friendship.views import FriendshipView
from users.views import UsernameCheckView, CustomUserViewSet, CountryListView, CityListView

router = SimpleRouter()
router.register(r'api/v1/users', CustomUserViewSet, basename='user')
router.register(r'api/v1/friendship', FriendshipView, basename='friendship')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/countries/', cache_page(60 * 15)(CountryListView.as_view()), name='country-list'),
    path('api/v1/cities/', cache_page(60 * 15)(CityListView.as_view()), name='city-list'),
    path('api/v1/check-username/<str:username>/', cache_page(60 * 15)(UsernameCheckView.as_view()), name='check-username'),
    path('api/v1/users/', include('djoser.urls.jwt')),
]

urlpatterns += router.urls
urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]