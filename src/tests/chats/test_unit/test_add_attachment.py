from io import BytesIO

import pytest
from rest_framework import status
from rest_framework.reverse import reverse

from core.utils.enums import AttachmentTypeEnum
from tests.factories.chat import ChatFactory
from tests.factories.user import UserFactory


@pytest.mark.django_db
def test__add_attachment__when_any_file(api_client):
    user = UserFactory()
    chat = ChatFactory(users=[user])
    data = BytesIO(b"test_file")
    data.name = "file.txt"
    data.seek(0)
    payload = {"file": data}

    api_client.force_authenticate(user=user)
    response = api_client.post(
        reverse(
            "chat-add-attachment",
            [
                chat.pk,
            ],
        ),
        data=payload,
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["chat"] == chat.pk
    assert response.data["user"] == user.pk
    assert response.data["file"]
    assert response.data["type"] == AttachmentTypeEnum.FILE


@pytest.mark.django_db
def test__add_attachment__when_any_file(api_client):
    user = UserFactory()
    chat = ChatFactory(users=[user])
    data = BytesIO(b"test_file")
    data.name = "file.txt"
    data.seek(0)
    payload = {"file": data}

    api_client.force_authenticate(user=user)
    response = api_client.post(
        reverse(
            "chat-add-attachment",
            [
                chat.pk,
            ],
        ),
        data=payload,
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["chat"] == chat.pk
    assert response.data["user"] == user.pk
    assert response.data["file"]
    assert response.data["type"] == AttachmentTypeEnum.PICTURE


@pytest.mark.django_db
def test__add_attachment__when_not_auth(api_client):
    user = UserFactory()
    chat = ChatFactory(users=[user])
    data = BytesIO(b"test_file")
    data.name = "file.txt"
    data.seek(0)
    payload = {"file": data}

    response = api_client.post(
        reverse(
            "chat-add-attachment",
            [
                chat.pk,
            ],
        ),
        data=payload,
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test__add_attachment__when_user_is_not_chat_member(api_client):
    users = UserFactory.create_batch(2)
    chat = ChatFactory(users=[users[0]])
    data = BytesIO(b"test_file")
    data.name = "file.txt"
    data.seek(0)
    payload = {"file": data}

    api_client.force_authenticate(user=users[1])
    response = api_client.post(
        reverse(
            "chat-add-attachment",
            [
                chat.pk,
            ],
        ),
        data=payload,
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["non_field_errors"][0] == "User is not a member of the chosen chats"


@pytest.mark.django_db
def test__add_attachment_when_chat_not_found(api_client):
    users = UserFactory.create_batch(2)
    ChatFactory(users=[users[0], users[1]])
    data = BytesIO(b"test_file")
    data.name = "file.txt"
    data.seek(0)
    payload = {"file": data}
    not_existing_chat_pk = 2

    api_client.force_authenticate(user=users[1])
    response = api_client.post(
        reverse(
            "chat-add-attachment",
            [
                not_existing_chat_pk,
            ],
        ),
        data=payload,
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
