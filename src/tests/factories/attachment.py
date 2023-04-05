import factory
from factory import SubFactory

from core.models.attachment import Attachment
from tests.factories.chat import ChatFactory
from tests.factories.user import UserFactory


class AttachmentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Attachment

    chat = SubFactory(ChatFactory)
    user = SubFactory(UserFactory)
