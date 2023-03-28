import json

from channels.generic.websocket import AsyncWebsocketConsumer
from loguru import logger


class BaseConsumer(AsyncWebsocketConsumer):
    group_name: str

    async def connect(self):
        pk = self.scope["url_route"]["kwargs"]["pk"]
        self.group_name = self.key_schema.get_key(pk)
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()
        logger.info("connected to ws")

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)
        logger.info("ws disconnected")

    async def chat_message(self, event):
        logger.info(f"ws send: {event['content']}")
        await self.send(text_data=json.dumps(event["content"]))
