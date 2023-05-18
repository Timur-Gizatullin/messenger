import os

import django

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.sessions import CookieMiddleware
from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "messenger.settings")
django.setup()
django_asgi_app = get_asgi_application()

from api.urls import websocket_urlpatterns  # noqa: E402
from core.middlewares.cookie_auth_middleware import CookieAuthTokenMiddleware  # noqa: E402

application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": (CookieMiddleware(CookieAuthTokenMiddleware((URLRouter(websocket_urlpatterns))))),
    }
)
