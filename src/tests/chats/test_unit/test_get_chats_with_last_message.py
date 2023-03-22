import pytest
from rest_framework import status
from rest_framework.reverse import reverse

from tests.factories.chat import ChatFactory
from tests.factories.user import UserFactory

from tests.confest import api_client


@pytest.mark.django_db
def test__get_chat_list_success_case(api_client):
    user = UserFactory(email="testt@test.test", password="test")
    ChatFactory.create_batch(3, users=UserFactory.create_batch(3))
    ChatFactory.create_batch(2, users=[user])
    expected_chats_len = 2

    api_client.force_authenticate(user=user)
    response = api_client.get(path=reverse("chat-list"))

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == expected_chats_len


def test__list_error_case(api_client):
    response = api_client.get(path=reverse("chat-list"))

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
