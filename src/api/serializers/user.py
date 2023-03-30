from rest_framework import serializers
from stdimage.validators import MaxSizeValidator, MinSizeValidator

from core.models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['pk', 'email', "profile_picture"]


class UploadProfilePictureSerializer(serializers.ModelSerializer):
    profile_picture = serializers.ImageField(required=True)

    class Meta:
        model = User
        fields = ["pk", "email", "profile_picture", ]
        extra_kwargs = {"email": {"read_only": True}}

    def create(self, validated_data):
        user = self.context["request"].user
        user.profile_picture = validated_data["profile_picture"]
        user.save()

        return user
