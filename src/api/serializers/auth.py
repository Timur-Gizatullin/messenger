from rest_framework import serializers
from rest_framework.authtoken.models import Token

from core.models import User, Chat


class AuthSignUpSerializer(serializers.ModelSerializer):
    password_repeat = serializers.CharField()

    def create(self, validated_data):
        user = User.objects.create_user(email=validated_data["email"])
        user.set_password(validated_data["password"])

        self_chat = Chat.objects.create()

        user.save()

        self_chat.users.set([user])
        self_chat.save()

        return user

    def validate(self, attrs):
        password_repeat = attrs.pop("password_repeat")
        if attrs["password"] != password_repeat:
            raise serializers.ValidationError("Passwords are not similar")

        return attrs

    class Meta:
        model = User
        fields = ["pk", "email", "password", "password_repeat"]


class AuthUserOutputSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["pk", "email", "token"]
        extra_kwargs = {"email": {"read_only": True}}

    def get_token(self, user: User) -> str:
        tokens = Token.objects.get_or_create(user=user)

        return tokens[0].key
