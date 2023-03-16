import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import  get_channel_layer

from loguru import logger

from api.serializers.message import MessageSerializer


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

        logger.info("connected to ws")

    async def receive(self, content):
        logger.info(content)

        serializer = self.get_serializer(data=content)

        if not serializer.is_valid():
            return

        group_name = serializer.get_group_name()

        self.groups.append(group_name)

        await self.channel_layer.group_add(
            group_name,
            self.channel_name,
        )

    async def notify(self, event):
        logger.info(event)
        await self.send_json(event["content"])

    async def add_message(self, message):
        serializer = MessageSerializer(message)
        group_name = serializer.get_group_name()
        chanel_layer = get_channel_layer()
        content = {
            "type": "add_message",
            "payload": serializer.data,
        }

        await chanel_layer.group_send(group_name, {
            "type": "notify",
            "content": content,
        })
