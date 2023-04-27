from channels.db import database_sync_to_async
from channels.sessions import CookieMiddleware, SessionMiddleware
from django.contrib.auth.models import AnonymousUser
from loguru import logger
from rest_framework.authtoken.models import Token

from core.models import User


@database_sync_to_async
def get_user(auth_token):
    try:
        return User.objects.get(pk=Token.objects.get(key=auth_token).user_id)
    except User.DoesNotExist or Token.DoesNotExist:
        logger.error("Invalid token")
        return AnonymousUser()


class CookieAuthMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        auth_token = scope["cookies"].get("X-Authorization", None)

        if not auth_token:
            logger.error("Missing token")
            scope["user"] = AnonymousUser()
        else:
            scope["user"] = await get_user(auth_token)

        return await self.app(scope, receive, send)


def AuthMiddlewareStack(inner):
    return CookieMiddleware(SessionMiddleware(CookieAuthMiddleware(inner)))
