import pytest
from rest_framework import status
from rest_framework.reverse import reverse

from tests.confest import api_client
from tests.factories.chat import ChatFactory
from tests.factories.message import MessageFactory
from tests.factories.user import UserFactory


@pytest.mark.parametrize(
    ("limit_offset", "expected_len"), [("?limit=10&offset=40", 4), ("?limit=10&offset=0", 10), ("", 44)]
)
@pytest.mark.django_db
def test__get_messages_with_pagination_list_success_case(limit_offset, expected_len, api_client):
    chat = ChatFactory()
    user = UserFactory()
    MessageFactory.create_batch(44, author_id=user.pk, chat_id=chat.pk)

    api_client.force_authenticate(user=user)
    response = api_client.get(path=f'{reverse("message-list")}{limit_offset}')

    assert response.status_code == status.HTTP_200_OK
    if limit_offset != "":
        assert len(response.data["results"]) == expected_len
    else:
        assert len(response.data) == expected_len


def test__get_messages_with_pagination_list_error_case(api_client):
    response = api_client.get(path=reverse("message-list"))

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
