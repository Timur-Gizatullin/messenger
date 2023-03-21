from typing import List

import pytest

from tests.factories import ChatFactory, UserFactory
from tests.confest import api_client


def get_users() -> List[UserFactory]:
    users = []
    for i in range(3):
        users.append(UserFactory(email=f"test{i}"))
    return users


def get_chats() -> List[ChatFactory]:
    chats = []
    for i in range(3):
        chats.append(ChatFactory())
    return chats


def set_chat_users(chats, users, current_user):
    chats_len = len(chats)
    for i in range(chats_len - 1):
        chats[i].users.set(users)
    chats[chats_len - 1].users.set([current_user])


@pytest.mark.django_db
def test_list_authenticated(api_client):
    user = UserFactory(email="testt@test.test", password="test")
    users = get_users()
    chats = get_chats()
    set_chat_users(chats, users, user)
    path = "/api/chats/"
    api_client.force_authenticate(user=user)

    response = api_client.get(path=path)

    assert response.data is not None
    assert len(response.data) == 1
    assert response.status_code == 200


def test_list_unauthorized(api_client):
    path = "/api/chats/"

    response = api_client.get(path=path)

    assert response.status_code == 401
