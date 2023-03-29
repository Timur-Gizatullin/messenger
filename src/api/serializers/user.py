from rest_framework import serializers
from stdimage.validators import MaxSizeValidator, MinSizeValidator

from core.models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['pk', 'email', "profile_picture"]


class UploadProfilePicSerializer(serializers.ModelSerializer):
    profile_picture = serializers.ImageField(
        required=True, validators=[MinSizeValidator(200, 100), MaxSizeValidator(1028, 768)]
    )

    class Meta:
        model = User
        fields = ["pk", "email", "profile_picture", ]
        extra_kwargs = {"email": {"read_only": True}}

    def create(self, validated_data):
        user = self.context["request"].user
        picture = validated_data["profile_picture"]
        user.save()
        user.profile_picture = picture

        return user
