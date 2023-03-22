import factory

from core.models import Chat
from tests.factories.user import UserFactory


class ChatFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Chat

    class Params:
        users = factory.SubFactory(UserFactory)

    @classmethod
    def create(cls, **kwargs):
        chat = super(ChatFactory, cls).create(**kwargs)
        users = kwargs.get("users", None)

        if users:
            chat.users.set(users)

        return chat
