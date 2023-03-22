from typing import List

import factory

from core.models import Chat, User, Message
from tests.factories.mixins import UniqueStringMixin


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    email = UniqueStringMixin("email")


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


class MessageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Message

