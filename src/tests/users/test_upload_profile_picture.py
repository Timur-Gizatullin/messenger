import tempfile
from io import BytesIO

import pytest
from django.core.files.uploadedfile import InMemoryUploadedFile, SimpleUploadedFile
from PIL import Image
from rest_framework import status
from rest_framework.reverse import reverse

from core.models import User
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
)
@pytest.mark.django_db
def test__upload_profile_picture__success_case(size, api_client):
    user = UserFactory()
    image_data = BytesIO()
    image_data.name = "test.png"
    image = Image.new("RGB", size, "white")
    image.save(image_data, format="png")
    image_data.seek(0)
    payload = {"profile_picture": image_data}

    api_client.force_authenticate(user=user)
    response = api_client.post(reverse("user-upload-profile-picture"), data=payload)

    assert response.status_code == status.HTTP_200_OK
    assert user.profile_picture is not None
    assert response.data["pk"] == user.pk


@pytest.mark.parametrize(
    "size",
    [
        [
            100,
            50,
        ],
        [
            1030,
            768,
        ],
        [
            1028,
            800,
        ],
    ],
)
@pytest.mark.django_db
def test__upload_profile_picture__when_wrong_size(size, api_client):
    user = UserFactory()
    image_data = BytesIO()
    image_data.name = "test.png"
    image = Image.new("RGB", size, "white")
    image.save(image_data, format="png")
    image_data.seek(0)
    payload = {"profile_picture": image_data}

    api_client.force_authenticate(user=user)
    response = api_client.post(reverse("user-upload-profile-picture"), data=payload)

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test__upload_profile_picture__when_pic_not_send(api_client):
    user = UserFactory()

    api_client.force_authenticate(user=user)
    response = api_client.post(reverse("user-upload-profile-picture"), format="multipart")

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test__upload_profile_picture__when_user_not_auth(api_client):
    image_data = BytesIO()
    image = Image.new("RGB", (200, 100), "white")
    image.save(image_data, format="png")
    image_data.seek(0)

    payload = {"profile_picture": SimpleUploadedFile("test.png", image_data.read(), content_type="image/png")}

    response = api_client.post(reverse("user-upload-profile-picture"), payload, format="multipart")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
