"""
URL configuration for user_service project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.template.defaulttags import url
from django.urls import path, include
from rest_framework.routers import SimpleRouter

from users.views import UsernameCheckView, CustomUserViewSet, CountryListView, CityListView, SendFriendRequestView, \
    CancelFriendRequestView

router = SimpleRouter()
router.register(r'api/v1/users', CustomUserViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/countries/', CountryListView.as_view(), name='country-list'),
    path('api/v1/cities/', CityListView.as_view(), name='city-list'),
    path('api/v1/check-username/<str:username>/', UsernameCheckView.as_view(), name='check-username'),
    path('api/v1/users/', include('djoser.urls.jwt')),
    path('api/v1/users/send_friend_request/', SendFriendRequestView.as_view(), name='send-friend-request'),
    path('api/v1/users/cancel_friend_request/', CancelFriendRequestView.as_view(), name='cancel-friend-request')
]

urlpatterns += router.urls