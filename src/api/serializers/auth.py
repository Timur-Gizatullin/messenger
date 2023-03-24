from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.authtoken.models import Token

from core.models import Chat, User


class AuthSignUpSerializer(serializers.ModelSerializer):
    password_repeat = serializers.CharField()

    def create(self, data):
        user = User.objects.create_user(email=data["email"])
        user.set_password(data["password"])

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


class AuthSignInSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def create(self, validated_data):
        return validated_data["user"]

    def validate(self, attrs):
        email = attrs.pop("email")
        password = attrs.pop("password")

        user = authenticate(email=email, password=password)

        if not user:
            raise serializers.ValidationError("Check login or password")

        attrs["user"] = user

        return attrs
