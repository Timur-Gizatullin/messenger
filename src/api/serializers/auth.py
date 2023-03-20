from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework import serializers

from core.models import User, Chat


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
        extra_kwargs = {
            "password": {"write_only": True, "required": True},
            "email": {"required": True},
        }


class AuthUserOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email"]
        extra_kwargs = {"email": {"read_only": True}}


class AuthSignInSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def create(self, data):
        request = self.context["request"]
        user = data["user"]

        token = Token.objects.get_or_create(user=user)

        return token[0].pk

    def validate(self, attrs):
        email = attrs.pop("email")
        password = attrs.pop("password")

        user = authenticate(email=email, password=password)

        if not user:
            raise serializers.ValidationError("Check login or password")

        attrs["user"] = user

        return attrs
