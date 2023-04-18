from dataclasses import asdict
from typing import List

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

from core.utils.data_classes import WSContent, WSMessage
from core.utils.enums import Action
from core.utils.key_schemas import BaseKeySchema


class WebSocketDistributorMixin:
    key_schema: BaseKeySchema

    def distribute_to_ws_consumers(self, data: dict, action: Action, postfix: List[str]) -> None:
        channel_layer = get_channel_layer()

        group_name = self.key_schema.get_key(postfix=postfix)

        content = WSContent(type=action, data=data)
        message = WSMessage(type="chat.message", content=content)

        async_to_sync(channel_layer.group_send)(group_name, asdict(message))


class ChatWebSocketDistributorMixin(WebSocketDistributorMixin):
    key_schema = BaseKeySchema(prefix="chat")


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
