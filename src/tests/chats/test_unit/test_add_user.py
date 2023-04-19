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
    admin = UserFactory()
    random_user_ids = [user.pk for user in UserFactory.create_batch(size=2)]
    chat = ChatFactory(users=[owner, admin])
    user_chat_owner = UserChat.objects.get(chat=chat.pk, user=owner)
    user_chat_owner.role = ChatRoleEnum.OWNER
    user_chat_owner.save()
    user_chat_admin = UserChat.objects.get(chat=chat.pk, user=admin)
    user_chat_admin.role = ChatRoleEnum.ADMIN
    user_chat_admin.save()
    random_user_ids.append(owner.pk)
    random_user_ids.append(admin.pk)

    api_client.force_authenticate(user=owner)
    response = api_client.patch(
        reverse(
            "chat-add-user",
            [
                chat.pk,
            ],
        ),
        data={"user_ids": random_user_ids},
        format="json",
    )

    assert response.status_code == status.HTTP_200_OK
    assert user_chat_owner.role == ChatRoleEnum.OWNER
    assert user_chat_admin.role == ChatRoleEnum.ADMIN
    assert UserChat.objects.get(chat=chat.pk, user=random_user_ids[0]).role == ChatRoleEnum.MEMBER
    assert UserChat.objects.get(chat=chat.pk, user=random_user_ids[1]).role == ChatRoleEnum.MEMBER


@pytest.mark.django_db
def test__add_user__when_admin_act(api_client):
    owner = UserFactory()
    admin = UserFactory()
    random_user_ids = [user.pk for user in UserFactory.create_batch(size=2)]
    chat = ChatFactory(users=[owner, admin])
    user_chat_owner = UserChat.objects.get(chat=chat.pk, user=owner)
    user_chat_owner.role = ChatRoleEnum.OWNER
    user_chat_owner.save()
    user_chat_admin = UserChat.objects.get(chat=chat.pk, user=admin)
    user_chat_admin.role = ChatRoleEnum.ADMIN
    user_chat_admin.save()
    random_user_ids.append(owner.pk)
    random_user_ids.append(admin.pk)

    api_client.force_authenticate(user=admin)
    response = api_client.patch(
        reverse(
            "chat-add-user",
            [
                chat.pk,
            ],
        ),
        data={"user_ids": random_user_ids},
        format="json",
    )

    assert response.status_code == status.HTTP_200_OK
    assert user_chat_owner.role == ChatRoleEnum.OWNER
    assert user_chat_admin.role == ChatRoleEnum.ADMIN
    assert UserChat.objects.get(chat=chat.pk, user=random_user_ids[0]).role == ChatRoleEnum.MEMBER
    assert UserChat.objects.get(chat=chat.pk, user=random_user_ids[1]).role == ChatRoleEnum.MEMBER


@pytest.mark.django_db
def test__add_user__when_not_owner_or_admin_act(api_client):
    user = UserFactory()
    random_user_ids = [user.pk for user in UserFactory.create_batch(size=2)]
    chat = ChatFactory(users=[user])

    api_client.force_authenticate(user=user)
    response = api_client.patch(
        reverse(
            "chat-add-user",
            [
                chat.pk,
            ],
        ),
        data={"user_ids": random_user_ids},
        format="json",
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["non_field_errors"][0] == constants.YOU_CANNOT_ADD_USERS_TO_THE_CHAT


@pytest.mark.django_db
def test__add_user_when_chat_not_exist(api_client):
    user = UserFactory()
    random_user_ids = [user.pk for user in UserFactory.create_batch(size=2)]
    not_existing_chat_id = 2

    api_client.force_authenticate(user=user)
    response = api_client.patch(
        reverse(
            "chat-add-user",
            [
                not_existing_chat_id,
            ],
        ),
        data={"user_ids": random_user_ids},
        format="json",
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test__add_user_when_user_is_not_chat_member(api_client):
    user = UserFactory()
    random_user_ids = [user.pk for user in UserFactory.create_batch(size=2)]
    chat = ChatFactory()

    api_client.force_authenticate(user=user)
    response = api_client.patch(
        reverse(
            "chat-add-user",
            [
                chat.pk,
            ],
        ),
        data={"user_ids": random_user_ids},
        format="json",
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test__add_user_when_not_auth(api_client):
    random_user_ids = [user.pk for user in UserFactory.create_batch(size=2)]
    chat = ChatFactory()

    response = api_client.patch(
        reverse(
            "chat-add-user",
            [
                chat.pk,
            ],
        ),
        data={"user_ids": random_user_ids},
        format="json",
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
