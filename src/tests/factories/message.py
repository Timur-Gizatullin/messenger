import factory

from core.models import Message
from tests.factories.mixins import UniqueStringMixin


class MessageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Message

    text = UniqueStringMixin("text")
