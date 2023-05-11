import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "messenger.settings")
django.setup()

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.sessions import CookieMiddleware
from django.core.asgi import get_asgi_application

django_asgi_app = get_asgi_application()

from api.urls import websocket_urlpatterns
from core.middlewares.cookie_auth_middleware import CookieAuthTokenMiddleware

application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": (CookieMiddleware(CookieAuthTokenMiddleware((URLRouter(websocket_urlpatterns))))),
    }
)
