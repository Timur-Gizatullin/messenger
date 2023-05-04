from random import randint

import pytest
from rest_framework import status
from rest_framework.reverse import reverse

from core.models import Message
from tests.factories.message import MessageFactory
from tests.factories.user import UserFactory


@pytest.mark.django_db
def test__delete_message__when_user_is_author(api_client):
    message_len_list = 10
    expected_len_queryset = 9
    author = UserFactory()
    message = MessageFactory.create_batch(message_len_list, author=author, chat__users=[author])

    message_to_delete_index = randint(1, message_len_list - 1)
    api_client.force_authenticate(author)
    response = api_client.delete(reverse("message-delete-message", args=[message[message_to_delete_index].pk]))

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Message.objects.all().count() == expected_len_queryset
    assert Message.objects.all().filter(pk=message[message_to_delete_index].pk).count() == 0


@pytest.mark.django_db
def test__delete_message__when_user_is_forwarder(api_client):
    message_len_list = 10
    expected_len_queryset = 9
    author = UserFactory()
    forwarded_by = UserFactory()
    message = MessageFactory.create_batch(
        message_len_list, author=author, forwarded_by=forwarded_by, chat__users=[author, forwarded_by]
    )

    message_to_delete_index = randint(1, message_len_list - 1)
    api_client.force_authenticate(forwarded_by)
    response = api_client.delete(reverse("message-delete-message", args=[message[message_to_delete_index].pk]))

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Message.objects.all().count() == expected_len_queryset
    assert Message.objects.all().filter(pk=message[message_to_delete_index].pk).count() == 0


@pytest.mark.django_db
def test__delete_message__when_user_is_author_and_forwarder(api_client):
    message_len_list = 10
    expected_len_queryset = 9
    author = UserFactory()
    message = MessageFactory.create_batch(message_len_list, author=author, forwarded_by=author, chat__users=[author])

    message_to_delete_index = randint(1, message_len_list - 1)
    api_client.force_authenticate(author)
    response = api_client.delete(reverse("message-delete-message", args=[message[message_to_delete_index].pk]))

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Message.objects.all().count() == expected_len_queryset
    assert Message.objects.all().filter(pk=message[message_to_delete_index].pk).count() == 0


@pytest.mark.django_db
def test__delete_message__when_user_is_not_chat_member(api_client):
    message_len_list = 10
    author = UserFactory()
    forwarded_by = UserFactory()
    not_chat_member = UserFactory()
    message = MessageFactory.create_batch(message_len_list, author=author, forwarded_by=forwarded_by)

    message_to_delete_index = randint(1, message_len_list - 1)
    api_client.force_authenticate(not_chat_member)
    response = api_client.delete(reverse("message-delete-message", args=[message[message_to_delete_index].pk]))

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert Message.objects.all().filter(pk=message[message_to_delete_index].pk)


@pytest.mark.django_db
def test__delete_message__when_user_is_chat_member_but_not_author(api_client):
    message_len_list = 10
    author = UserFactory()
    chat_member = UserFactory()
    message = MessageFactory.create_batch(message_len_list, author=author, chat__users=[author, chat_member])

    message_to_delete_index = randint(1, message_len_list - 1)
    api_client.force_authenticate(chat_member)
    response = api_client.delete(reverse("message-delete-message", args=[message[message_to_delete_index].pk]))

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert Message.objects.all().filter(pk=message[message_to_delete_index].pk)
