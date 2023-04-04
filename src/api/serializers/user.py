from rest_framework import serializers

from core.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["pk", "email", "profile_picture"]


class UploadProfilePictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["pk", "email", "profile_picture", "thumbnail_profile_picture"]
        extra_kwargs = {"email": {"read_only": True}, "profile_picture": {"required": True}}

    def create(self, validated_data):
        user = self.context["request"].user
        user.profile_picture = validated_data["profile_picture"]
        user.save()

        return user
