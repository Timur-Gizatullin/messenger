import pytest
from rest_framework import status
from rest_framework.reverse import reverse

from tests.factories.chat import ChatFactory
from tests.factories.message import MessageFactory
from tests.factories.user import UserFactory


@pytest.mark.django_db
def test__add_message__when_author_is_not_chat_member(api_client):
    user = UserFactory()
    chat = ChatFactory()

    api_client.force_authenticate(user=user)
    response = api_client.post(reverse("chat-add-message", args=[chat.pk]), data={"text": "any message", })

    assert response.status_code == status.HTTP_400_BAD_REQUEST
