from typing import Any

from channels.db import database_sync_to_async
from channels.routing import URLRouter
from channels.sessions import CookieMiddleware, SessionMiddleware
from django.contrib.auth.models import AnonymousUser
from loguru import logger
from rest_framework.authtoken.models import Token

from core.models import User


@database_sync_to_async
def get_user(auth_token) -> AnonymousUser | User:
    try:
        return User.objects.get(pk=Token.objects.get(key=auth_token).user_id)
    except (User.DoesNotExist, Token.DoesNotExist):
        logger.error(f"Invalid token: {auth_token}")
        return AnonymousUser()


class CookieAuthTokenMiddleware:
    def __init__(self, inner: URLRouter):
        self.inner = inner

    async def __call__(self, scope: dict, receive: callable, send: callable) -> None:
        auth_token = scope["cookies"].get("auth_token", None)

        if not auth_token:
            logger.error("Missing token")
            scope["user"] = AnonymousUser()
        else:
            scope["user"] = await get_user(auth_token)

        return await self.inner(scope, receive, send)
