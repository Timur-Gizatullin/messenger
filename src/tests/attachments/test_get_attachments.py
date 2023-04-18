import pytest
from rest_framework import status
from rest_framework.reverse import reverse

from tests.factories.attachment import AttachmentFactory
from tests.factories.chat import ChatFactory
from tests.factories.user import UserFactory


@pytest.mark.parametrize(("limit", "offset", "expected_len"), [(10, 0, 10), (0, 0, 33), (10, 30, 3)])
@pytest.mark.django_db
def test__get_attachment__when_user_is_a_chat_member(limit, offset, expected_len, api_client):
    user = UserFactory()
    chat = ChatFactory.create_batch(2, users=[user])
    AttachmentFactory.create_batch(33, author=user, chat=chat[0])
    AttachmentFactory.create_batch(22, author=user, chat=chat[1])

    api_client.force_authenticate(user=user)
    response = api_client.get(reverse("chat-get-attachments", args=[chat[0].pk]), {"limit": limit, "offset": offset})

    assert response.status_code == status.HTTP_200_OK
    if not (limit == 0 and offset == 0):
        assert len(response.data["results"]) == expected_len
        for result in response.data["results"]:
            assert result["chat"] == chat[0].pk
    else:
        assert len(response.data) == expected_len
        for data in response.data:
            assert data["chat"] == chat[0].pk


@pytest.mark.parametrize(("limit", "offset", "expected_len"), [(10, 0, 0), (0, 0, 0), (10, 30, 0)])
@pytest.mark.django_db
def test__get_attachment__when_user_is_not_a_chat_member(limit, offset, expected_len, api_client):
    user = UserFactory()
    user_member = UserFactory()
    chat = ChatFactory.create_batch(2, users=[user_member])
    AttachmentFactory.create_batch(33, author=user_member, chat=chat[0])
    AttachmentFactory.create_batch(22, author=user_member, chat=chat[1])

    api_client.force_authenticate(user=user)
    response = api_client.get(reverse("chat-get-attachments", args=[chat[0].pk]), {"limit": limit, "offset": offset})

    assert response.status_code == status.HTTP_200_OK
    if not (limit == 0 and offset == 0):
        assert len(response.data["results"]) == expected_len
    else:
        assert len(response.data) == expected_len


def test__get_attachment__without_auth(api_client):
    response = api_client.get(reverse("chat-get-attachments", args=[42]))

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
