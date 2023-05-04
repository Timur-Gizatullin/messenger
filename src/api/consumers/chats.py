import json

from loguru import logger

from api.consumers.base import BaseConsumer
from core.utils.key_schemas import BaseKeySchema


class UserChatsConsumer(BaseConsumer):
    key_schema = BaseKeySchema(prefix="user")

    def get_group_name(self):
        return self.key_schema.get_key(postfix=[str(self.scope["url_route"]["kwargs"]["pk"])])

    async def chat_chats(self, event):
        logger.info(f"ws send {event['content']} to group {self.group_name}")
        await self.send(text_data=json.dumps(event["content"]))
