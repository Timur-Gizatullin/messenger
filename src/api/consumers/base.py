import json

from channels.generic.websocket import AsyncWebsocketConsumer
from loguru import logger


class BaseConsumer(AsyncWebsocketConsumer):
    group_name: str

    def get_group_name(self):
        raise NotImplementedError()

    async def connect(self):
        self.user = self.scope["user"]
        self.group_name = self.get_group_name()
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()
        logger.info(f"ws connected to group: {self.group_name}")

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)
        logger.info(f"ws disconnected from group: {self.group_name}")

    async def chat_message(self, event):
        logger.info(f"ws send {event['content']} to group {self.group_name}")
        await self.send(text_data=json.dumps(event["content"]))
