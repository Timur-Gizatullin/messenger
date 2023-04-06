import pytest
from rest_framework import status
from rest_framework.reverse import reverse

from tests.conftest import get_image_data
from tests.factories.user import UserFactory


@pytest.mark.parametrize(
    "size",
    [
        [
            200,
            100,
        ],
        [
            1028,
            768,
        ],
        [
            350,
            400,
        ],
    ],
    ids=["small_size", "large_size", "medium_size"],
)
@pytest.mark.django_db
def test__upload_profile_picture__success_case(size, api_client):
    user = UserFactory()
    payload = {"picture_to_upload": get_image_data(size=size)}

    api_client.force_authenticate(user=user)
    response = api_client.post(reverse("user-upload-profile-picture"), data=payload)

    assert response.status_code == status.HTTP_200_OK
    assert user.profile_picture is not None
    assert response.data["pk"] == user.pk
    assert response.data["profile_picture"]
    assert response.data["profile_picture"]["original"] == user.profile_picture.url
    assert response.data["profile_picture"]["thumbnail"] == user.profile_picture.thumbnail.url


@pytest.mark.django_db
def test__upload_profile_picture__when_picture_not_send(api_client):
    user = UserFactory()

    api_client.force_authenticate(user=user)
    response = api_client.post(reverse("user-upload-profile-picture"))

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test__upload_profile_picture__when_user_not_auth(api_client):
    payload = {"picture_to_upload": get_image_data(size=(200, 100))}

    response = api_client.post(reverse("user-upload-profile-picture"), payload)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
