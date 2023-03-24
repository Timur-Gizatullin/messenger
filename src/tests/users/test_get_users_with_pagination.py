import pytest
from rest_framework import status
from rest_framework.reverse import reverse

from tests.factories.user import UserFactory


@pytest.mark.parametrize(("limit", "offset", "expected_len"), [(10, 0, 10), (0, 0, 42), (10, 40, 2)])
@pytest.mark.django_db
def test__get_users_with_pagination__success_case(limit, offset, expected_len, api_client):
    users = UserFactory.create_batch(42)

    api_client.force_authenticate(user=users[0])
    response = api_client.get(reverse("user-list"), {"limit": limit, "offset": offset})

    assert response.status_code == status.HTTP_200_OK
    if not (limit == 0 and offset == 0):
        assert len(response.data["results"]) == expected_len
    else:
        assert len(response.data) == expected_len


@pytest.mark.django_db
def test__get_users_with_pagination__when_not_auth(api_client):
    response = api_client.get(reverse("user-list"))

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
