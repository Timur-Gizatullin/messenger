from api.consumers.base import BaseConsumer
from core.utils.key_schemas import BaseKeySchema


class ChatConsumer(BaseConsumer):
    key_schema = BaseKeySchema(prefix="chat")
