import pytest
from rest_framework import status
from rest_framework.reverse import reverse

from tests.factories.chat import ChatFactory
from tests.factories.user import UserFactory


@pytest.mark.django_db
def test__get_chats_with_last_message__success_case(api_client):
    user = UserFactory(email="testt@test.test", password="test")
    ChatFactory.create_batch(3, users=UserFactory.create_batch(3))
    expected_chats = ChatFactory.create_batch(2, users=[user])
    expected_chats_len = 2

    api_client.force_authenticate(user=user)
    response = api_client.get(path=reverse("chat-list"))

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == expected_chats_len
    assert response.data[0]["pk"] == expected_chats[0].pk
    assert response.data[1]["pk"] == expected_chats[1].pk


def test__get_chats_with_last_message__without_auth(api_client):
    response = api_client.get(path=reverse("chat-list"))

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
