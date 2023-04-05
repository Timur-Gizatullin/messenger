from django.urls import path
from rest_framework import routers

from api.openapi import schema_view
from api.views import ChatViewSet
from api.views.attachment import AttachmentViewSet
from api.views.auth import AuthViewSet
from api.views.user import UserViewSet

router = routers.DefaultRouter()
router.register("chats", ChatViewSet, basename="chat")
router.register("auth", AuthViewSet, basename="auth")
router.register("users", UserViewSet, basename="user")
router.register("attachments", AttachmentViewSet, basename="attachment")

urlpatterns = router.urls
urlpatterns += [path("docs/", schema_view.with_ui("swagger", cache_timeout=0), name="swagger")]
