from django.urls import path
from rest_framework import routers

from api.openapi import schema_view
from api.views import ChatViewSet
from api.views.auth import AuthViewSet
from api.views.message import MessageViewSet

router = routers.DefaultRouter()
router.register("chats", ChatViewSet)
router.register("auth", AuthViewSet)
router.register("messages", MessageViewSet, basename="message")

urlpatterns = router.urls
urlpatterns += [path("docs/", schema_view.with_ui("swagger", cache_timeout=0), name="swagger")]

urlpatterns += [path("docs/", schema_view.with_ui("swagger", cache_timeout=0), name="swagger")]
