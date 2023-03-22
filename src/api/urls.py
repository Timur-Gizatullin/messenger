from django.urls import path
from rest_framework import routers

from api.openapi import schema_view
from api.views import ChatViewSet
from api.views.auth import AuthViewSet

router = routers.DefaultRouter()
router.register("chats", ChatViewSet, basename="chat")
router.register("auth", AuthViewSet)

urlpatterns = router.urls
urlpatterns += [path("docs/", schema_view.with_ui("swagger", cache_timeout=0), name="swagger")]

urlpatterns += [path("docs/", schema_view.with_ui("swagger", cache_timeout=0), name="swagger")]
