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
    chat_from_forward = ChatFactory(users=[users[0]])
    messages = MessageFactory.create_batch(5, author=users[0], chat=chat_from_forward)

    api_client.force_authenticate(users[0])
    response = api_client.post(
        reverse("message-forward"),
        data={
            "forward_to_chat_id": chat_to_forward.pk,
            "message_ids": [messages[0].pk, messages[1].pk, messages[2].pk],
        },
        format="json",
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert len(response.data) == 3
    for message in response.data:
        assert message["forwarded_by"] == users[0].pk
        assert message["chat"] == chat_to_forward.pk


@pytest.mark.django_db
def test__forward_message__when_message_ids_not_filled(api_client):
    users = UserFactory.create_batch(10)
    chat_to_forward = ChatFactory(users=[users[0]])
    MessageFactory.create_batch(5, author=users[0], chat__users=[users[0], users[1]])

    api_client.force_authenticate(users[0])
    response = api_client.post(
        reverse("message-forward"),
        data={
            "forward_to_chat_id": chat_to_forward.pk,
            "message_ids": list(),
        },
        format="json",
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["non_field_errors"][0] == "message_ids field is required"


@pytest.mark.django_db
def test__forward_message__when_message_ids_missed(api_client):
    users = UserFactory.create_batch(10)
    chat_to_forward = ChatFactory(users=[users[0]])
    MessageFactory.create_batch(5, author=users[0], chat__users=[users[0], users[1]])

    api_client.force_authenticate(users[0])
    response = api_client.post(
        reverse("message-forward"),
        data={"forward_to_chat_id": chat_to_forward.pk},
        format="json",
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["message_ids"][0] == "This field is required."


@pytest.mark.django_db
def test__forward_message__when_not_auth(api_client):
    users = UserFactory.create_batch(10)
    chat_to_forward = ChatFactory(users=[users[0]])
    messages = MessageFactory.create_batch(5, author=users[0], chat__users=[users[0], users[1]])

    response = api_client.post(
        reverse("message-forward"),
        data={
            "forward_to_chat_id": chat_to_forward.pk,
            "message_ids": [messages[0].pk, messages[1].pk, messages[2].pk],
        },
        format="json",
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


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
            "forward_to_chat_id": chat_to_forward.pk,
            "message_ids": [messages[0].pk, messages[1].pk, messages[2].pk],
        },
        format="json",
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["non_field_errors"][0] == "User is not a member of the chat to forward"


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
            "forward_to_chat_id": chat_to_forward.pk,
            "message_ids": [messages[0].pk, messages[1].pk, messages[2].pk],
        },
        format="json",
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["non_field_errors"][0] == "User is not a member of the current chat"


@pytest.mark.django_db
def test__forward_message__when_user_is_not_a_member_of_initial_chat(api_client):
    users = UserFactory.create_batch(10)
    chat_to_forward = ChatFactory(users=[users[0]])
    messages = MessageFactory.create_batch(5, author=users[0], chat__users=[users[2], users[1]])

    api_client.force_authenticate(users[0])
    response = api_client.post(
        reverse("message-forward"),
        data={
            "forward_to_chat_id": chat_to_forward.pk,
            "message_ids": [messages[0].pk, messages[1].pk, messages[2].pk],
        },
        format="json",
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["non_field_errors"][0] == "User is not a member of the current chat"
