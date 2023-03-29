import pytest
from rest_framework import status
from rest_framework.reverse import reverse

from tests.factories.user import UserFactory


@pytest.mark.parametrize(
    ("limit", "offset", "user_email", "expected_len"),
    [
        (10, 0, "", 10),
        (0, 0, "", 45),
        (10, 40, "", 5),
        (0, 0, "qw", 3),
        (0, 0, "qwer", 3),
        (0, 0, "qwertla1", 1),
        (0, 0, "", 45),
        (10, 0, "qw", 3),
        (4, 1, "qwer", 2),
    ],
)
@pytest.mark.django_db
def test__get_users__success_case(limit, offset, user_email, expected_len, api_client):
    users = UserFactory.create_batch(42)
    users_to_find = UserFactory.create_batch(3)
    for i in range(len(users_to_find)):
        users_to_find[i].email = f"qwertla{i}@example.com"
        users_to_find[i].save()

    api_client.force_authenticate(user=users[0])
    response = api_client.get(reverse("user-list"), {"limit": limit, "offset": offset, "email": user_email})

    assert response.status_code == status.HTTP_200_OK
    if not (limit == 0 and offset == 0):
        assert len(response.data["results"]) == expected_len
    else:
        assert len(response.data) == expected_len


@pytest.mark.django_db
def test__get_users__when_not_auth(api_client):
    response = api_client.get(reverse("user-list"))

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
