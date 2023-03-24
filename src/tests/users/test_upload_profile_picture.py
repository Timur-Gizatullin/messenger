import io

import pytest
from rest_framework import status
from rest_framework.reverse import reverse

from core.models import User
from tests.factories.user import UserFactory


@pytest.mark.django_db
def test__upload_profile_picture__success_case(api_client):
    user = UserFactory()
    image_name = "fake-image-stream.jpg"
    data = {"image": (io.BytesIO(b"i_am_fake_image"), image_name)}

    api_client.force_authenticate(user=user)
    response = api_client.patch(reverse("user-upload-profile-picture"), data=data)

    assert response.status_code == status.HTTP_200_OK
    patched_user = User.objects.get(pk=user.pk)
    assert patched_user.profile_picture is not None
