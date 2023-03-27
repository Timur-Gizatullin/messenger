import json

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from core.utils.key_schemas import BaseKeySchema


class WebSocketDistributorMixin:
    def distribute_to_ws_consumers(self, data):
        channel_layer = get_channel_layer()

        group_name = self.key_schema.get_key(data["chat"])
        data = json.dumps(data)

        async_to_sync(channel_layer.group_send)(
            group_name,
            {
                "type": "chat.message",
                "content": data,
            },
        )


class ChatWebSocketMixin(WebSocketDistributorMixin):
    key_schema = BaseKeySchema(prefix="chat")
