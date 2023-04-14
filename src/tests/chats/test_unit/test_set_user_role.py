import pytest
from rest_framework import status
from rest_framework.reverse import reverse

from core import constants
from core.models.user_chat import UserChat
from core.utils.enums import ChatRoleEnum
from tests.factories.chat import ChatFactory
from tests.factories.user import UserFactory


@pytest.mark.parametrize("current_user_chat_role", ["ADMIN", "MEMBER"])
@pytest.mark.django_db
def test__set_user_role__when_user_is_admin(api_client, current_user_chat_role):
    owner = UserFactory()
    user_to_update = UserFactory()
    chat = ChatFactory(users=[owner, user_to_update])
    owner_chat = UserChat.objects.filter(chat=chat).filter(user=owner).get()
    owner_chat.role = ChatRoleEnum.OWNER
    owner_chat.save()

    api_client.force_authenticate(user=owner)
    response = api_client.patch(
        reverse("chat-set-user-role", [chat.pk, user_to_update.pk]), data={"role": current_user_chat_role}
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.data["chat"] == chat.pk
    assert response.data["user"] == user_to_update.pk
    assert response.data["role"] == current_user_chat_role


@pytest.mark.parametrize("current_user_chat_role", ["ADMIN", "MEMBER"])
@pytest.mark.django_db
def test__set_user_role__when_user_is_owner(api_client, current_user_chat_role):
    admin = UserFactory()
    user_to_update = UserFactory()
    chat = ChatFactory(users=[admin, user_to_update])
    admin_chat = UserChat.objects.filter(chat=chat).filter(user=admin).get()
    admin_chat.role = ChatRoleEnum.ADMIN
    admin_chat.save()

    api_client.force_authenticate(user=admin)
    response = api_client.patch(
        reverse("chat-set-user-role", [chat.pk, user_to_update.pk]), data={"role": current_user_chat_role}
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.data["chat"] == chat.pk
    assert response.data["user"] == user_to_update.pk
    assert response.data["role"] == current_user_chat_role


@pytest.mark.parametrize("current_user_chat_role", ["ADMIN", "MEMBER", "OWNER"])
@pytest.mark.django_db
def test__set_user_role__when_user_is_member(api_client, current_user_chat_role):
    member = UserFactory()
    user_to_update = UserFactory()
    chat = ChatFactory(users=[member, user_to_update])

    api_client.force_authenticate(user=member)
    response = api_client.patch(
        reverse("chat-set-user-role", [chat.pk, user_to_update.pk]), data={"role": current_user_chat_role}
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["non_field_errors"][0] == constants.YOU_CANNOT_SET_THE_ROLE_OF_OTHERS_USERS_OF_THIS_CHAT


@pytest.mark.parametrize("current_user_chat_role", ["ADMIN", "MEMBER", "OWNER"])
@pytest.mark.django_db
def test__set_user_role__when_admin_updating_owner(api_client, current_user_chat_role):
    admin = UserFactory()
    user_to_update = UserFactory()
    chat = ChatFactory(users=[admin, user_to_update])
    admin_chat = UserChat.objects.filter(chat=chat).filter(user=admin).get()
    admin_chat.role = ChatRoleEnum.ADMIN
    admin_chat.save()
    owner_chat = UserChat.objects.filter(chat=chat).filter(user=user_to_update).get()
    owner_chat.role = ChatRoleEnum.OWNER
    owner_chat.save()

    api_client.force_authenticate(user=admin)
    response = api_client.patch(
        reverse("chat-set-user-role", [chat.pk, user_to_update.pk]), data={"role": current_user_chat_role}
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["non_field_errors"][0] == constants.OWNER_ROLE_IS_IMMUTABLE


@pytest.mark.django_db
def test__set_user_role__when_new_role_is_owner(api_client):
    admin = UserFactory()
    user_to_update = UserFactory()
    chat = ChatFactory(users=[admin, user_to_update])
    admin_chat = UserChat.objects.filter(chat=chat).filter(user=admin).get()
    admin_chat.role = ChatRoleEnum.ADMIN
    admin_chat.save()

    api_client.force_authenticate(user=admin)
    response = api_client.patch(reverse("chat-set-user-role", [chat.pk, user_to_update.pk]), data={"role": "OWNER"})

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["non_field_errors"][0] == constants.OWNER_IS_NOT_ALLOWED_AS_CHOICE


@pytest.mark.django_db
def test__set_user_role__when_not_auth(api_client):
    user = UserFactory()
    user_to_update = UserFactory()
    chat = ChatFactory(users=[user, user_to_update])

    response = api_client.patch(reverse("chat-set-user-role", [chat.pk, user_to_update.pk]), data={"role": "OWNER"})

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
