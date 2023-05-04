import os

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.sessions import CookieMiddleware
from django.core.asgi import get_asgi_application

from api.urls import websocket_urlpatterns
from core.middlewares.cookie_auth_middleware import CookieAuthTokenMiddleware

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "messenger.settings")

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": (CookieMiddleware(CookieAuthTokenMiddleware((URLRouter(websocket_urlpatterns))))),
    }
)
