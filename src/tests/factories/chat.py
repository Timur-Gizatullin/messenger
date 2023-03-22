import factory

from core.models import Chat


class ChatFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Chat
