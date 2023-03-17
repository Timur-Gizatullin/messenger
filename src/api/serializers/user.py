from rest_framework import serializers

from core.models import User


class AuthSignUpSerializer(serializers.ModelSerializer):
    password_repeat = serializers.CharField(write_only=True, min_length=8, max_length=128,
                                            required=True, trim_whitespace=True)

    def create(self, data):
        user = User.objects.create_user(email=data['email'])
        user.set_password(data['password'])
        return user

    def validate(self, attrs):
        password_repeat = attrs.pop("password_repeat")
        if attrs['password'] != password_repeat:
            raise serializers.ValidationError("Passwords are not similar")

        return attrs

    class Meta:
        model = User
        fields = ['pk', 'email', 'password', 'password_repeat']
        extra_kwargs = {
            'password': {'write_only': True, "required": True, "min_length": 8},
            'email': {"required": True}
        }
