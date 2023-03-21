import factory

from core.models import Chat, User, Message


class ChatFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Chat


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User


class MessageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Message
