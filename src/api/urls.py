from django.urls import path
from rest_framework import routers

from api.openapi import schema_view
from api.views import ChatViewSet, AuthViewSet

router = routers.DefaultRouter()
router.register(r'chats', ChatViewSet)
router.register(r'auth', AuthViewSet)

urlpatterns = router.urls
urlpatterns += [
    path("docs/", schema_view.with_ui("swagger", cache_timeout=0), name="swagger")
]
