import pytest
from rest_framework import status
from rest_framework.reverse import reverse

from core.utils.enums import AttachmentTypeEnum
from tests.conftest import get_image_data, get_test_data_file
from tests.factories.attachment import AttachmentFactory
from tests.factories.chat import ChatFactory
from tests.factories.message import MessageFactory
from tests.factories.user import UserFactory


@pytest.mark.django_db
def test__add_attachment__when_not_picture(api_client):
    user = UserFactory()
    chat = ChatFactory(users=[user])
    payload = {"file": get_test_data_file(), "chat": chat.pk}

    api_client.force_authenticate(user=user)
    response = api_client.post(
        reverse(
            "attachment-list",
        ),
        data=payload,
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["chat"] == chat.pk
    assert response.data["created_by"] == user.pk
    assert response.data["file"]
    assert response.data["type"] == AttachmentTypeEnum.FILE


@pytest.mark.django_db
def test__add_attachment__when_picture(api_client):
    user = UserFactory()
    chat = ChatFactory(users=[user])
    payload = {"file": get_image_data((100, 200)), "chat": chat.pk}

    api_client.force_authenticate(user=user)
    response = api_client.post(
        reverse(
            "attachment-list",
        ),
        data=payload,
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["chat"] == chat.pk
    assert response.data["created_by"] == user.pk
    assert response.data["file"]
    assert response.data["type"] == AttachmentTypeEnum.PICTURE


@pytest.mark.django_db
def test__add_attachment__when_reply_to_message_given(api_client):
    user = UserFactory()
    replier = UserFactory()
    chat = ChatFactory(users=[user, replier])
    message = MessageFactory(author=user, chat=chat)
    payload = {"file": get_test_data_file(), "chat": chat.pk, "reply_to_message": message.pk}

    api_client.force_authenticate(user=replier)
    response = api_client.post(
        reverse(
            "attachment-list",
        ),
        data=payload,
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["chat"] == chat.pk
    assert response.data["created_by"] == replier.pk
    assert response.data["file"]
    assert response.data["type"] == AttachmentTypeEnum.FILE
    assert response.data["reply_to_message"] == message.pk


@pytest.mark.django_db
def test__add_attachment__when_reply_to_attachment_given(api_client):
    user = UserFactory()
    replier = UserFactory()
    chat = ChatFactory(users=[user, replier])
    attachment = AttachmentFactory(created_by=user, chat=chat)
    payload = {"file": get_test_data_file(), "chat": chat.pk, "reply_to_attachment": attachment.pk}

    api_client.force_authenticate(user=replier)
    response = api_client.post(
        reverse(
            "attachment-list",
        ),
        data=payload,
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["chat"] == chat.pk
    assert response.data["created_by"] == replier.pk
    assert response.data["file"]
    assert response.data["type"] == AttachmentTypeEnum.FILE
    assert response.data["reply_to_attachment"] == attachment.pk


@pytest.mark.django_db
def test__add_attachment__when_reply_to_attachment_and_reply_to_message_given(api_client):
    user = UserFactory()
    replier = UserFactory()
    chat = ChatFactory(users=[user, replier])
    attachment = AttachmentFactory(created_by=user, chat=chat)
    message = MessageFactory(author=user, chat=chat)
    payload = {
        "file": get_test_data_file(),
        "chat": chat.pk,
        "reply_to_attachment": attachment.pk,
        "reply_to_message": message.pk,
    }

    api_client.force_authenticate(user=replier)
    response = api_client.post(
        reverse(
            "attachment-list",
        ),
        data=payload,
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["non_field_errors"][0] == "Choose only one object to reply"


@pytest.mark.django_db
def test__add_attachment__when_reply_to_attachment_is_not_part_of_chat(api_client):
    user = UserFactory()
    replier = UserFactory()
    chat = ChatFactory(users=[user, replier])
    random_attachment = AttachmentFactory(created_by=user, chat=ChatFactory(users=[user, replier]))
    payload = {"file": get_test_data_file(), "chat": chat.pk, "reply_to_attachment": random_attachment.pk}

    api_client.force_authenticate(user=replier)
    response = api_client.post(
        reverse(
            "attachment-list",
        ),
        data=payload,
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["non_field_errors"][0] == "Chosen object is not part of chat"


@pytest.mark.django_db
def test__add_attachment__when_reply_to_message_is_not_part_of_chat(api_client):
    user = UserFactory()
    replier = UserFactory()
    chat = ChatFactory(users=[user, replier])
    random_message = MessageFactory(author=user, chat=ChatFactory(users=[user, replier]))
    payload = {"file": get_test_data_file(), "chat": chat.pk, "reply_to_message": random_message.pk}

    api_client.force_authenticate(user=replier)
    response = api_client.post(
        reverse(
            "attachment-list",
        ),
        data=payload,
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["non_field_errors"][0] == "Chosen object is not part of chat"


@pytest.mark.django_db
def test__add_attachment__when_not_auth(api_client):
    user = UserFactory()
    chat = ChatFactory(users=[user])
    payload = {"file": get_test_data_file(), "chat": chat.pk}

    response = api_client.post(
        reverse(
            "attachment-list",
        ),
        data=payload,
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test__add_attachment__when_user_is_not_chat_member(api_client):
    users = UserFactory.create_batch(2)
    chat = ChatFactory(users=[users[0]])
    payload = {"file": get_test_data_file(), "chat": chat.pk}

    api_client.force_authenticate(user=users[1])
    response = api_client.post(
        reverse(
            "attachment-list",
        ),
        data=payload,
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["non_field_errors"][0] == "User is not a member of the chosen chats"


@pytest.mark.django_db
def test__add_attachment_when_chat_not_found(api_client):
    users = UserFactory.create_batch(2)
    ChatFactory(users=[users[0], users[1]])
    not_existing_chat_pk = 2
    payload = {"file": get_test_data_file(), "chat": not_existing_chat_pk}

    api_client.force_authenticate(user=users[1])
    response = api_client.post(
        reverse(
            "attachment-list",
        ),
        data=payload,
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["chat"][0] == f'Invalid pk "{not_existing_chat_pk}" - object does not exist.'
