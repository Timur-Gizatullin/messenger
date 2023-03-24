import pytest
from rest_framework import status
from rest_framework.reverse import reverse

from core.models import Message
from tests.factories.chat import ChatFactory
from tests.factories.message import MessageFactory
from tests.factories.user import UserFactory


@pytest.mark.django_db
def test__delete_message__when_user_is_author(api_client):
    author = UserFactory()
    message = MessageFactory.create_batch(10, author=author, chat__users=[author])

    api_client.force_authenticate(author)
    response = api_client.delete(reverse("chat-delete-message", args=[message[3].chat.pk, message[3].pk]))

    assert response.status_code == status.HTTP_204_NO_CONTENT
    queryset = Message.objects.all()
    assert queryset.count() == 9
    assert len(queryset.filter(pk=message[3].pk)) == 0


@pytest.mark.django_db
def test__delete_message__when_user_is_forwarder(api_client):
    author = UserFactory()
    forwarded_by = UserFactory()
    message = MessageFactory.create_batch(
        10, author=author, forwarded_by=forwarded_by, chat__users=[author, forwarded_by]
    )

    api_client.force_authenticate(forwarded_by)
    response = api_client.delete(reverse("chat-delete-message", args=[message[3].chat.pk, message[3].pk]))

    assert response.status_code == status.HTTP_204_NO_CONTENT
    queryset = Message.objects.all()
    assert queryset.count() == 9
    assert len(queryset.filter(pk=message[3].pk)) == 0


@pytest.mark.django_db
def test__delete_message__when_user_is_not_chat_member(api_client):
    author = UserFactory()
    forwarded_by = UserFactory()
    not_chat_member = UserFactory()
    message = MessageFactory.create_batch(10, author=author, forwarded_by=forwarded_by)

    api_client.force_authenticate(not_chat_member)
    response = api_client.delete(reverse("chat-delete-message", args=[message[3].chat.pk, message[3].pk]))

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test__delete_message__when_user_is_chat_member_but_not_author(api_client):
    author = UserFactory()
    chat_member = UserFactory()
    message = MessageFactory.create_batch(10, author=author, chat__users=[author, chat_member])

    api_client.force_authenticate(chat_member)
    response = api_client.delete(reverse("chat-delete-message", args=[message[3].chat.pk, message[3].pk]))

    assert response.status_code == status.HTTP_404_NOT_FOUND
