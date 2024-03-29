from django.urls import path
from rest_framework import routers

from api.consumers.chat import ChatConsumer
from api.consumers.user_chats import UserChatsConsumer
from api.openapi import schema_view
from api.views import ChatViewSet
from api.views.attachment import AttachmentViewSet
from api.views.auth import AuthViewSet
from api.views.message import MessageViewSet
from api.views.user import UserViewSet

router = routers.DefaultRouter()
router.register("chats", ChatViewSet, basename="chat")
router.register("auth", AuthViewSet, basename="auth")
router.register("users", UserViewSet, basename="user")
router.register("messages", MessageViewSet, basename="message")
router.register("attachments", AttachmentViewSet, basename="attachment")

urlpatterns = router.urls
urlpatterns += [path("docs/", schema_view.with_ui("swagger", cache_timeout=0), name="swagger")]

websocket_urlpatterns = [
    path(r"ws/chat/<int:pk>", ChatConsumer.as_asgi()),
    path(r"ws/user/<int:pk>/chats", UserChatsConsumer.as_asgi()),
]
