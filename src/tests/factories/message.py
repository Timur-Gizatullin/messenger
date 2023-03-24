import factory

from core.models import Message


class MessageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Message
