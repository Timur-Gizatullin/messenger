from rest_framework import serializers

from core.models import User


class UserSerializer(serializers.ModelSerializer):
    def create(self, data):
        user = User.objects.create_user(
            email=data['email'],
            password=data['password'],
        )

        return user

    class Meta:
        model = User
        fields = ['pk', 'email', 'password', 'repeat_password']
        extra_kwargs = {
            'password': {'write_only': True},
            'password_repeat': {'write_only': True},
        }
