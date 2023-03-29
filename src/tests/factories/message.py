import factory
from factory import SubFactory

from core.models import Message
from tests.factories.chat import ChatFactory
from tests.factories.mixins import UniqueStringMixin


class MessageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Message

    chat = SubFactory(ChatFactory)
    text = UniqueStringMixin("text")
