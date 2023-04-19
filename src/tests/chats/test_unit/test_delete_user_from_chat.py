import pytest
from rest_framework import status
from rest_framework.reverse import reverse

from core import constants
from core.models.user_chat import UserChat
from core.utils.enums import ChatRoleEnum
from tests.factories.chat import ChatFactory
from tests.factories.user import UserFactory


@pytest.mark.django_db
def test__delete_user_from_chat__when_owner_act(api_client):
    owner = UserFactory()
    users = UserFactory.create_batch(size=10)
    users.append(owner)
    chat = ChatFactory(users=users)
    user_chat_owner = UserChat.objects.get(user=owner, chat=chat)
    user_chat_owner.role = ChatRoleEnum.OWNER
    user_chat_owner.save()
    user_to_delete_id = users[5].pk

    api_client.force_authenticate(user=owner)
    response = api_client.delete(reverse("chat-delete-user", [chat.pk, user_to_delete_id]))

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert UserChat.objects.all().count() == 10
    assert not UserChat.objects.filter(user__id=user_to_delete_id, chat=chat)


@pytest.mark.django_db
def test__delete_user_from_chat__when_admin_act(api_client):
    admin = UserFactory()
    users = UserFactory.create_batch(size=10)
    users.append(admin)
    chat = ChatFactory(users=users)
    user_chat_admin = UserChat.objects.get(user=admin, chat=chat)
    user_chat_admin.role = ChatRoleEnum.ADMIN
    user_chat_admin.save()
    user_to_delete_id = users[5].pk

    api_client.force_authenticate(user=admin)
    response = api_client.delete(reverse("chat-delete-user", [chat.pk, user_to_delete_id]))

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert UserChat.objects.all().count() == 10
    assert not UserChat.objects.filter(user__id=user_to_delete_id, chat=chat)


@pytest.mark.django_db
def test__delete_user_from_chat__when_current_user_is_not_owner_or_admin(api_client):
    users = UserFactory.create_batch(size=2)
    chat = ChatFactory(users=[users[0], users[1]])

    api_client.force_authenticate(user=users[0])
    response = api_client.delete(reverse("chat-delete-user", [chat.pk, users[1].pk]))

    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json() == constants.YOU_HAVE_NO_PERMISSION_TO_DELETE_USER


@pytest.mark.django_db
def test__delete_user_from_chat__when_user_to_delete_is_owner(api_client):
    users = UserFactory.create_batch(size=2)
    chat = ChatFactory(users=[users[0], users[1]])
    user_chat_admin = UserChat.objects.get(user=users[0], chat=chat)
    user_chat_admin.role = ChatRoleEnum.ADMIN
    user_chat_admin.save()
    user_chat_owner = UserChat.objects.get(user=users[1], chat=chat)
    user_chat_owner.role = ChatRoleEnum.OWNER
    user_chat_owner.save()

    api_client.force_authenticate(user=users[0])
    response = api_client.delete(reverse("chat-delete-user", [chat.pk, users[1].pk]))

    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json() == constants.YOU_CANNOT_DELETE_CHAT_OWNER


@pytest.mark.django_db
def test__delete_user_from_chat__when_current_user_is_not_chat_member(api_client):
    users = UserFactory.create_batch(size=2)
    chat = ChatFactory(users=[users[1]])

    api_client.force_authenticate(user=users[0])
    response = api_client.delete(reverse("chat-delete-user", [chat.pk, users[1].pk]))

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test__delete_user_from_chat__when_user_to_delete_is_not_chat_member(api_client):
    users = UserFactory.create_batch(size=2)
    chat = ChatFactory(users=[users[0]])

    api_client.force_authenticate(user=users[0])
    response = api_client.delete(reverse("chat-delete-user", [chat.pk, users[1].pk]))

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test__delete_user_from_chat__when_not_auth(api_client):
    users = UserFactory.create_batch(size=2)
    chat = ChatFactory(users=[users[0]])

    response = api_client.delete(reverse("chat-delete-user", [chat.pk, users[1].pk]))

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
