import debug_toolbar
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.views.decorators.cache import cache_page
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf.urls.static import static

from friendship.urls import friendship_urlpatterns
from users.urls import users_urlpatterns
from users.views import CountryListView, CityListView

schema_view = get_schema_view(
    openapi.Info(
        title="user-service API",
        default_version='v1',
        description="API для управления пользователями, а также для сервиса дружбы.",
        terms_of_service="None",
        contact=openapi.Contact(email="bronyboy2014@gmail.com"),
        license=openapi.License(name="Лицензия"),
    ),
    public=True,
    # permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('__debug__/', include(debug_toolbar.urls)),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    path('api/v1/countries/', cache_page(60 * 15)(CountryListView.as_view()), name='country-list'),
    path('api/v1/cities/', cache_page(60 * 15)(CityListView.as_view()), name='city-list'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += users_urlpatterns
urlpatterns += friendship_urlpatterns
