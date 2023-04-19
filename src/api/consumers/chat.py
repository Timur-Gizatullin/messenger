from api.consumers.base import BaseConsumer
from core.utils.key_schemas import BaseKeySchema


class ChatConsumer(BaseConsumer):
    key_schema = BaseKeySchema(prefix="chat")

    def get_group_name(self):
        return self.key_schema.get_key(postfix=[str(self.scope["url_route"]["kwargs"]["pk"])])
