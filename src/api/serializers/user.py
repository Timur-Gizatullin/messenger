from rest_framework import serializers

from core.models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['pk', 'email', "profile_picture", 'password']
        extra_kwargs = {'password': {'write_only': True}}
