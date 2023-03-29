import pytest
from rest_framework import status
from rest_framework.reverse import reverse

from tests.factories.chat import ChatFactory
from tests.factories.message import MessageFactory
from tests.factories.user import UserFactory


@pytest.mark.django_db
def test__forward_message__success_case(api_client):
    users = UserFactory.create_batch(10)
    chat_to_forward = ChatFactory(users=[users[0]])
    messages = MessageFactory.create_batch(5, author=users[0], chat__users=[users[0], users[1]])

    api_client.force_authenticate(users[0])
    response = api_client.post(
        reverse("message-forward"),
        data={
            "forward_to": chat_to_forward.pk,
            "message_ids": [{"pk": messages[0].pk}, {"pk": messages[1].pk}, {"pk": messages[2].pk}],
        },
        format="json",
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert len(response.data) == 3


@pytest.mark.django_db
def test__forward_message__when_user_is_not_a_member_of_chat_to_forward(api_client):
    users = UserFactory.create_batch(10)
    chat_to_forward = ChatFactory(
        users=[
            users[1],
        ]
    )
    messages = MessageFactory.create_batch(5, author=users[0], chat__users=[users[0], users[1]])

    api_client.force_authenticate(users[0])
    response = api_client.post(
        reverse("message-forward"),
        data={
            "forward_to": chat_to_forward.pk,
            "message_ids": [{"pk": messages[0].pk}, {"pk": messages[1].pk}, {"pk": messages[2].pk}],
        },
        format="json",
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test__forward_message__when_user_is_not_a_member_of_any_chat(api_client):
    users = UserFactory.create_batch(10)
    chat_to_forward = ChatFactory(
        users=[
            users[1],
        ]
    )
    messages = MessageFactory.create_batch(5, author=users[0], chat__users=[users[1]])

    api_client.force_authenticate(users[0])
    response = api_client.post(
        reverse("message-forward"),
        data={
            "forward_to": chat_to_forward.pk,
            "message_ids": [{"pk": messages[0].pk}, {"pk": messages[1].pk}, {"pk": messages[2].pk}],
        },
        format="json",
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test__forward_message__when_user_is_not_a_member_of_initial_chat(api_client):
    users = UserFactory.create_batch(10)
    chat_to_forward = ChatFactory(users=[users[0]])
    messages = MessageFactory.create_batch(5, author=users[0], chat__users=[users[2], users[1]])
    expected_error_content = b'{"non_field_errors":["Can\'t reach the message"]}'

    api_client.force_authenticate(users[0])
    response = api_client.post(
        reverse("message-forward"),
        data={
            "forward_to": chat_to_forward.pk,
            "message_ids": [{"pk": messages[0].pk}, {"pk": messages[1].pk}, {"pk": messages[2].pk}],
        },
        format="json",
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.content == expected_error_content
