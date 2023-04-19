import pytest
from rest_framework import status
from rest_framework.reverse import reverse

from core.models.attachment import Attachment
from tests.factories.attachment import AttachmentFactory
from tests.factories.user import UserFactory


@pytest.mark.django_db
def test__delete_attachment__success_case(api_client):
    user = UserFactory()
    attachment_to_delete = AttachmentFactory(author=user, chat__users=[user])

    api_client.force_authenticate(user=user)
    response = api_client.delete(reverse("attachment-delete-attachment", [attachment_to_delete.pk]))

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Attachment.objects.filter(pk=attachment_to_delete.pk).count() == 0


@pytest.mark.django_db
def test__delete_attachment__when_user_is_not_chat_member(api_client):
    user = UserFactory()
    attachment_to_delete = AttachmentFactory(author=user)

    api_client.force_authenticate(user=user)
    response = api_client.delete(reverse("attachment-delete-attachment", [attachment_to_delete.pk]))

    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test__delete_attachment__when_user_is_not_attachment_owner(api_client):
    user = UserFactory()
    attachment_to_delete = AttachmentFactory(chat__users=[user])

    api_client.force_authenticate(user=user)
    response = api_client.delete(reverse("attachment-delete-attachment", [attachment_to_delete.pk]))

    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test__delete_attachment__when_user_is_not_attachment_owner_and_not_chat_member(api_client):
    user = UserFactory()
    attachment_to_delete = AttachmentFactory()

    api_client.force_authenticate(user=user)
    response = api_client.delete(reverse("attachment-delete-attachment", [attachment_to_delete.pk]))

    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test__delete_attachment__when_its_not_exist(api_client):
    user = UserFactory()
    not_existing_attachment_pk = 42

    api_client.force_authenticate(user=user)
    response = api_client.delete(reverse("attachment-delete-attachment", [not_existing_attachment_pk]))

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test__delete_attachment__when_not_auth(api_client):
    user = UserFactory()
    attachment_to_delete = AttachmentFactory(chat__users=[user])

    response = api_client.delete(reverse("attachment-delete-attachment", [attachment_to_delete.pk]))

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
