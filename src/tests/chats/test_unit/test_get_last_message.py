import pytest

from api.serializers.chat import ChatSerializer
from tests.factories.chat import ChatFactory
from tests.factories.message import MessageFactory
from tests.factories.user import UserFactory


@pytest.mark.django_db
def test__get_last_message__when_exist():
    chat = ChatFactory()
    user = UserFactory()
    MessageFactory(author=user, chat=chat)
    last_message = MessageFactory(author=user, chat=chat)

    serializer = ChatSerializer(chat)

    assert serializer.data["last_message"].text == last_message.text


@pytest.mark.django_db
def test__get_last_message__when_not_exist():
    chat = ChatFactory()

    serializer = ChatSerializer(chat)

    assert serializer.data["last_message"] is None
