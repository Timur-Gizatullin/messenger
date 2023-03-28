from rest_framework import serializers
from stdimage.validators import MinSizeValidator, MaxSizeValidator

from core.models import User


class UploadProfilePicSerializer(serializers.ModelSerializer):
    profile_picture = serializers.ImageField(required=True,
                                             validators=[MinSizeValidator(200, 100), MaxSizeValidator(1028, 768)])

    class Meta:
        model = User
        fields = ["profile_picture", ]

    def create(self, validated_data):
        user = self.context["request"].user
        picture = validated_data["profile_picture"]
        user.profile_picture = picture
        user.save()

        return user
