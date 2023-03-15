from rest_framework import serializers

from core.models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['pk', 'email', 'password']
        extra_kwargs = {'password': {'write-only': True}}
