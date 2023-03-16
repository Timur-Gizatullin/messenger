import json
from channels.generic.websocket import AsyncWebsocketConsumer

from loguru import logger


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.chat_id = self.scope["url_route"]["kwargs"]["pk"]
        self.group_name = f"chat_{self.chat_id}"

        await self.channel_layer.group_add(self.group_name, self.channel_name)

        await self.accept()

        logger.info("connected to ws")

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

        logger.info("disconnected from ws")

    async def receive(self, text_data):
        logger.info(text_data)
        text_data_json = json.loads(text_data)
        message_text = text_data_json["text"]
        message_picture = text_data_json["picture"]
        user = text_data_json["author"]

        await self.channel_layer.group_send(
            self.group_name,
            {
                "type": "chat_message",
                "message_text": message_text,
                "message_picture": message_picture,
                "user": user,
            },
        )

    async def chat_message(self, event):
        logger.info(event)
        message_text = event["message_text"]
        message_picture = event["message_picture"]
        user = event["user"]
        await self.send(
            text_data=json.dumps(
                {
                    "message_text": message_text,
                    "message_picture": message_picture,
                    "user": user,
                }
            )
        )

        pass
