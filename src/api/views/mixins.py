import json
from dataclasses import asdict

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from core.utils.data_classes import WSContent, WSMessage
from core.utils.enums import Action
from core.utils.key_schemas import BaseKeySchema


class WebSocketDistributorMixin:
    def distribute_to_ws_consumers(self, data, action: Action):
        channel_layer = get_channel_layer()

        group_name = self.key_schema.get_key(data["chat"])
        data = json.dumps(data)

        content = WSContent(action, data)
        message = WSMessage("chat.message", content)

        async_to_sync(channel_layer.group_send)(
            group_name, asdict(message)
        )


class ChatWebSocketDistributorMixin(WebSocketDistributorMixin):
    key_schema = BaseKeySchema(prefix="chat")
