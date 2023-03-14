from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from core.models import Chat


class ChatSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    users = serializers.ManyRelatedField()
    last_message = serializers.CharField()

    class Meta:
        model = Chat
        fields = ['pk', 'users', 'last_message', 'is_dialog']
        depth = 1

        validators = [
            UniqueTogetherValidator(
                queryset=Chat.objects.all(),
                fields=['users', 'is_dialog']
            )
        ]
