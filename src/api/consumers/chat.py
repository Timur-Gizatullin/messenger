from channels.generic.websocket import AsyncWebsocketConsumer
from loguru import logger


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        pk = self.scope["url_route"]["kwargs"]["pk"]
        await self.channel_layer.group_add(f"chat_{pk}", self.channel_name)
        await self.accept()
        logger.info("connected to ws")

    async def disconnect(self, code):
        pk = self.scope["url_route"]["kwargs"]["pk"]
        await self.channel_layer.group_discard(f"chat_{pk}", self.channel_name)
        logger.info("ws disconnected")

    async def receive(self, text_data=None, bytes_data=None):
        logger.info(f"ws receive: {text_data}")
        pk = self.scope["url_route"]["kwargs"]["pk"]
        await self.channel_layer.group_send(
            f"chat_{pk}",
            {
                "type": "chat.notify",
                "message": text_data,
            },
        )

    async def chat_notify(self, event):
        logger.info(f"ws send: {event}")
        await self.send(text_data=event["content"])
