import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer, WebsocketConsumer
from channels.layers import  get_channel_layer

from loguru import logger

from api.serializers.message import MessageSerializer


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        logger.info("CONNECTeD TO WS")
        pk = self.scope['url_route']['kwargs']['pk']
        await self.channel_layer.group_add(f"chat_{pk}", self.channel_name)
        await self.accept()

    async def disconnect(self, code):
        logger.info("DISCARD WS")
        pk = self.scope['url_route']['kwargs']['pk']
        await self.channel_layer.group_discard(f"chat_{pk}", self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):
        logger.info(f"RECEIVE WS: {text_data}")
        pk = self.scope['url_route']['kwargs']['pk']
        await self.channel_layer.group_send(
            f"chat_{pk}",
            {
                "type": "chat.notify",
                "message": text_data,
            }
        )

    async def chat_notify(self, event):
        logger.info(f"SEND WS {event}")
        await self.send(text_data=event["content"])
