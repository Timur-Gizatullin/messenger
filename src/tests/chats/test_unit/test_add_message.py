import pytest
from rest_framework import status
from rest_framework.reverse import reverse

from tests.factories.chat import ChatFactory
from tests.factories.message import MessageFactory
from tests.factories.user import UserFactory


@pytest.mark.django_db
def test__add_message__when_text_filled(api_client):
    user = UserFactory()
    chat = ChatFactory(users=[user])
    payload = {
        "text": "any message",
    }

    api_client.force_authenticate(user=user)
    response = api_client.post(reverse("chat-add-message", args=[chat.pk]), data=payload)

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["text"] == payload["text"]
    assert response.data["author"] == user.pk
    assert response.data["chat"] == chat.pk


@pytest.mark.django_db
def test__add_message__when_text_is_empty(api_client):
    user = UserFactory()
    chat = ChatFactory(users=[user])
    payload = {
        "text": " ",
    }

    api_client.force_authenticate(user=user)
    response = api_client.post(reverse("chat-add-message", args=[chat.pk]), data=payload)

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test__add_message__when_text_and_replied_to_filled(api_client):
    user = UserFactory()
    chat = ChatFactory(users=[user])
    message = MessageFactory(author=UserFactory(), chat=chat)
    payload = {
        "replied_to": message.pk,
        "text": "any message",
    }

    api_client.force_authenticate(user=user)
    response = api_client.post(reverse("chat-add-message", args=[chat.pk]), data=payload)

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["text"] == payload["text"]
    assert response.data["author"] == user.pk
    assert response.data["chat"] == chat.pk
    assert response.data["replied_to"] == message.pk


@pytest.mark.django_db
def test__add_message__when_author_is_not_chat_member(api_client):
    user = UserFactory()
    chat = ChatFactory()
    payload = {
        "text": "any message",
    }

    api_client.force_authenticate(user=user)
    response = api_client.post(reverse("chat-add-message", args=[chat.pk]), data=payload)

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test__add_message__when_text_not_filled(api_client):
    user = UserFactory()
    chat = ChatFactory(users=[user])
    payload = {}

    api_client.force_authenticate(user=user)
    response = api_client.post(reverse("chat-add-message", args=[chat.pk]), data=payload)

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test__add_message__when_not_auth(api_client):
    chat = ChatFactory()
    payload = {
        "text": "any message",
    }

    response = api_client.post(reverse("chat-add-message", args=[chat.pk]), data=payload)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
