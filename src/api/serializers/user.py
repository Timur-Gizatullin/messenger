from rest_framework import serializers

from core.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["pk", "email", "profile_picture"]


class UploadProfilePictureSerializer(serializers.ModelSerializer):
    profile_picture_variants = serializers.DictField(read_only=True)

    class Meta:
        model = User
        fields = ["pk", "email", "profile_picture_variants", "profile_picture"]
        extra_kwargs = {"email": {"read_only": True}, "profile_picture": {"required": True, "write_only": True}}

    def create(self, validated_data):
        user = self.context["request"].user
        user.profile_picture = validated_data["profile_picture"]
        user.save()

        return user

    def to_representation(self, instance):
        representation = dict()
        picture_variations = dict()
        attrs = ["thumbnail", "large", "medium"]

        representation["pk"] = instance.pk
        representation["email"] = instance.email

        picture_variations["default"] = instance.profile_picture.url
        for attr in attrs:
            if hasattr(instance.profile_picture, attr):
                picture_variations[attr] = getattr(instance.profile_picture, attr).url

        representation["profile_picture_variants"] = picture_variations

        return representation
