import pytest
from rest_framework import status
from rest_framework.reverse import reverse

from core.models import User
from tests.factories.user import UserFactory


@pytest.mark.parametrize(("user_email", "expected_len"), [("qw", 3), ("qwer", 3), ("qwertla1", 1), ("", 45)])
@pytest.mark.django_db
def test__find_user__success_case(user_email, expected_len, api_client):
    users = UserFactory.create_batch(42)
    users_to_find = UserFactory.create_batch(3)
    for i in range(len(users_to_find)):
        users_to_find[i].email = f"qwertla{i}@example.com"
        users_to_find[i].save()

    api_client.force_authenticate(user=users[0])
    response = api_client.get(reverse("user-find-user"), {"email": user_email})

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == expected_len
