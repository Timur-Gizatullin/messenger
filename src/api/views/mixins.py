from dataclasses import asdict
from typing import List

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

from core.utils.data_classes import WSContent, WSMessage
from core.utils.enums import ActionEnum, WSType
from core.utils.key_schemas import BaseKeySchema


class WebSocketDistributorMixin:
    key_schema: BaseKeySchema

    @classmethod
    def distribute_to_ws_consumers(cls, data: dict, action: ActionEnum, postfix: List[str], ws_type: WSType) -> None:
        channel_layer = get_channel_layer()

        group_name = cls.key_schema.get_key(postfix=postfix)

        content = WSContent(type=action, data=data)
        message = WSMessage(type=ws_type, content=content)
        dic = asdict(message)

        async_to_sync(channel_layer.group_send)(group_name, asdict(message))


class ChatWebSocketDistributorMixin(WebSocketDistributorMixin):
    key_schema = BaseKeySchema(prefix="chat")


class UserChatsWebSocketDistributorMixin(WebSocketDistributorMixin):
    key_schema = BaseKeySchema(prefix="user")


class PaginateMixin:
    def get_paginated_queryset(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        paginator = LimitOffsetPagination()
        page = paginator.paginate_queryset(queryset, request, view=self)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
