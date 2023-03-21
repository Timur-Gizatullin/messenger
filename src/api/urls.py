from rest_framework import routers

from api.views import ChatViewSet
from api.views.message import MessageViewSet

router = routers.DefaultRouter()
router.register('chats', ChatViewSet)
router.register("messages", MessageViewSet)

urlpatterns = router.urls
