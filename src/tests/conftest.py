from io import BytesIO

import pytest
from PIL import Image
from rest_framework.test import APIClient


@pytest.fixture
def api_client() -> APIClient:
    return APIClient()


def get_image_data(size: tuple[int, int]) -> BytesIO:
    image_data = BytesIO()
    image_data.name = "test.png"
    image = Image.new("RGB", size)
    image.save(image_data, format="png")
    image_data.seek(0)
    return image_data


def get_data_file() -> BytesIO:
    data = BytesIO(b"test_file")
    data.name = "file.txt"
    data.seek(0)

    return data
