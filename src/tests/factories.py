import factory

from core.models import Chat, User


class ChatFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Chat


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
