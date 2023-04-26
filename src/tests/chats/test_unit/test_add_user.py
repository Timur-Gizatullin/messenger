import pytest
from rest_framework import status
from rest_framework.reverse import reverse

from core import constants
from core.models.user_chat import UserChat
from core.utils.enums import ChatRoleEnum
from tests.factories.chat import ChatFactory
from tests.factories.user import UserFactory


@pytest.mark.django_db
def test__add_user__when_owner_act(api_client):
    owner = UserFactory()
    user_to_add_ids = [user.pk for user in UserFactory.create_batch(size=2)]
    chat = ChatFactory(users=[owner])
    user_chat_owner = UserChat.objects.get(chat=chat.pk, user=owner)
    user_chat_owner.role = ChatRoleEnum.OWNER
    user_chat_owner.save()

    api_client.force_authenticate(user=owner)
    response = api_client.post(
        reverse(
            "chat-add-user",
            [
                chat.pk,
            ],
        ),
        data={"user_ids": user_to_add_ids},
        format="json",
    )

    assert response.status_code == status.HTTP_200_OK
    for user_id in user_to_add_ids:
        assert UserChat.objects.get(chat=chat.pk, user=user_id).role == ChatRoleEnum.MEMBER


@pytest.mark.django_db
def test__add_user__when_admin_act(api_client):
    admin = UserFactory()
    user_to_add_ids = [user.pk for user in UserFactory.create_batch(size=2)]
    chat = ChatFactory(users=[admin])
    user_chat_admin = UserChat.objects.get(chat=chat.pk, user=admin)
    user_chat_admin.role = ChatRoleEnum.ADMIN
    user_chat_admin.save()

    api_client.force_authenticate(user=admin)
    response = api_client.post(
        reverse(
            "chat-add-user",
            [
                chat.pk,
            ],
        ),
        data={"user_ids": user_to_add_ids},
        format="json",
    )

    assert response.status_code == status.HTTP_200_OK
    for user_id in user_to_add_ids:
        assert UserChat.objects.get(chat=chat.pk, user=user_id).role == ChatRoleEnum.MEMBER


@pytest.mark.django_db
def test__add_user__when_add_existing_users(api_client):
    admin = UserFactory()
    owner = UserFactory()
    user_to_add_ids = [user.pk for user in UserFactory.create_batch(size=2)]
    chat = ChatFactory(users=[admin, owner])
    user_chat_admin = UserChat.objects.get(chat=chat.pk, user=admin)
    user_chat_admin.role = ChatRoleEnum.ADMIN
    user_chat_admin.save()
    user_chat_owner = UserChat.objects.get(chat=chat.pk, user=owner)
    user_chat_owner.role = ChatRoleEnum.OWNER
    user_chat_owner.save()

    api_client.force_authenticate(user=admin)
    response = api_client.post(
        reverse(
            "chat-add-user",
            [
                chat.pk,
            ],
        ),
        data={"user_ids": user_to_add_ids},
        format="json",
    )

    assert response.status_code == status.HTTP_200_OK
    assert UserChat.objects.get(chat=chat, user=admin).role == ChatRoleEnum.ADMIN
    assert UserChat.objects.get(chat=chat, user=owner).role == ChatRoleEnum.OWNER


@pytest.mark.django_db
def test__add_user__when_not_owner_or_admin_act(api_client):
    user = UserFactory()
    user_to_add_ids = [user.pk for user in UserFactory.create_batch(size=2)]
    chat = ChatFactory(users=[user])

    api_client.force_authenticate(user=user)
    response = api_client.post(
        reverse(
            "chat-add-user",
            [
                chat.pk,
            ],
        ),
        data={"user_ids": user_to_add_ids},
        format="json",
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json()["detail"] == constants.ONLY_ADMIN_OR_OWNER_CAN_ADD_USERS_TO_CHAT


@pytest.mark.django_db
def test__add_user_when_chat_not_exist(api_client):
    user = UserFactory()
    user_to_add_ids = [user.pk for user in UserFactory.create_batch(size=2)]
    not_existing_chat_id = 2

    api_client.force_authenticate(user=user)
    response = api_client.post(
        reverse(
            "chat-add-user",
            [
                not_existing_chat_id,
            ],
        ),
        data={"user_ids": user_to_add_ids},
        format="json",
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test__add_user_when_user_is_not_chat_member(api_client):
    user = UserFactory()
    user_to_add_ids = [user.pk for user in UserFactory.create_batch(size=2)]
    chat = ChatFactory()

    api_client.force_authenticate(user=user)
    response = api_client.post(
        reverse(
            "chat-add-user",
            [
                chat.pk,
            ],
        ),
        data={"user_ids": user_to_add_ids},
        format="json",
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test__add_user_when_not_auth(api_client):
    user_to_add_ids = [user.pk for user in UserFactory.create_batch(size=2)]
    chat = ChatFactory()

    response = api_client.post(
        reverse(
            "chat-add-user",
            [
                chat.pk,
            ],
        ),
        data={"user_ids": user_to_add_ids},
        format="json",
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
