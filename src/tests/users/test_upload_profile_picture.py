from io import BytesIO

import pytest
from PIL import Image
from rest_framework import status
from rest_framework.reverse import reverse

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
    ids=["200, 100", "1028, 768", "350, 400"],
)
@pytest.mark.django_db
def test__upload_profile_picture__success_case(size, api_client):
    user = UserFactory()
    image_data = BytesIO()
    image_data.name = "test.png"
    image = Image.new("RGB", size)
    image.save(image_data, format="png")
    image_data.seek(0)
    payload = {"profile_picture": image_data}

    api_client.force_authenticate(user=user)
    response = api_client.post(reverse("user-upload-profile-picture"), data=payload)

    assert response.status_code == status.HTTP_200_OK
    assert user.profile_picture is not None
    assert response.data["pk"] == user.pk
    assert response.data["profile_picture"]


@pytest.mark.django_db
def test__upload_profile_picture__when_picture_not_send(api_client):
    user = UserFactory()

    api_client.force_authenticate(user=user)
    response = api_client.post(reverse("user-upload-profile-picture"))

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test__upload_profile_picture__when_user_not_auth(api_client):
    image_data = BytesIO()
    image_data.name = "test.png"
    image = Image.new("RGB", (200, 100))
    image.save(image_data, format="png")
    image_data.seek(0)
    payload = {"profile_picture": image_data}

    response = api_client.post(reverse("user-upload-profile-picture"), payload)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
