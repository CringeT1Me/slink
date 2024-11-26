from rest_framework.routers import SimpleRouter

from friendship.views import FriendshipView

router = SimpleRouter()
router.register(r'api/v1/friendship', FriendshipView, basename='friendship')

friendship_urlpatterns = []

friendship_urlpatterns += router.urls