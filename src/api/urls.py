from django.urls import path, re_path
from rest_framework import routers

from api.consumers.chat import ChatConsumer
from api.openapi import schema_view
from api.views import ChatViewSet

router = routers.DefaultRouter()
router.register(r"chats", ChatViewSet)

urlpatterns = router.urls
urlpatterns += [
    path("docs/", schema_view.with_ui("swagger", cache_timeout=0), name="swagger")
]

websocket_urlpatterns = [
    path(r"ws/chat/<int:pk>", ChatConsumer.as_asgi()),
]
