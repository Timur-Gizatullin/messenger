import pytest

from api.serializers.chat import ChatSerializer

from tests.factories.factories import ChatFactory, MessageFactory, UserFactory


@pytest.mark.django_db
def test__chat_serializer_get_last_message_when_exist():
    chat = ChatFactory()
    user = UserFactory()
    MessageFactory(text="PenultimateMessage", author=user, chat=chat)
    MessageFactory(text="LastMessage", author=user, chat=chat)

    serializer = ChatSerializer(chat)

    assert serializer.data["last_message"].text == "LastMessage"


@pytest.mark.django_db
def test__chat_serializer_get_last_message_when_none():
    chat = ChatFactory()

    serializer = ChatSerializer(chat)

    assert serializer.data["last_message"] is None
