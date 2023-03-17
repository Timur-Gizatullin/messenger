from rest_framework import serializers

from core.models import User


class AuthSignUpSerializer(serializers.ModelSerializer):
    def create(self, data):
        user = User.objects.create_user(email=data['email'])
        user.set_password(data['password'])
        return user

    def validate(self, attrs):
        if attrs['password'] != attrs['password_repeat']:
            raise serializers.ValidationError("Passwords are not similar")

    class Meta:
        model = User
        fields = ['pk', 'email', 'password', 'repeat_password']
        extra_kwargs = {
            'password': {'write_only': True, "required": True},
            'password_repeat': {'write_only': True, "required": True},
            'email': {"required": True}
        }
