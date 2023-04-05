from rest_framework import serializers

from api.serializers.image import StdImageSerializer
from core.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["pk", "email", "profile_picture"]


class UploadProfilePictureSerializer(serializers.ModelSerializer):
    profile_picture = StdImageSerializer(read_only=True)
    picture_to_upload = serializers.ImageField(write_only=True)

    class Meta:
        model = User
        fields = ["pk", "email", "profile_picture", "picture_to_upload"]
        extra_kwargs = {"email": {"read_only": True}}

    def create(self, validated_data):
        user = self.context["request"].user
        user.profile_picture = validated_data["picture_to_upload"]
        user.save()

        return user
