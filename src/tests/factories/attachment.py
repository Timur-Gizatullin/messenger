import factory
from factory import SubFactory

from core.models import Attachment
from tests.factories.chat import ChatFactory


class AttachmentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Attachment

    chat = SubFactory(ChatFactory)
