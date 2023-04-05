from rest_framework import serializers
from stdimage.models import StdImageFieldFile


class StdImageSerializer(serializers.Serializer):
    original = serializers.SerializerMethodField()
    thumbnail = serializers.SerializerMethodField()
    medium = serializers.SerializerMethodField()
    large = serializers.SerializerMethodField()

    def get_original(self, picture: StdImageFieldFile) -> str:
        return picture.url

    def get_thumbnail(self, picture: StdImageFieldFile) -> str | None:
        if hasattr(picture, "thumbnail"):
            return picture.thumbnail.url
        return None

    def get_medium(self, picture: StdImageFieldFile) -> str | None:
        if hasattr(picture, "medium"):
            return picture.medium.url
        return None

    def get_large(self, picture: StdImageFieldFile) -> str | None:
        if hasattr(picture, "large"):
            return picture.large.url
        return None
