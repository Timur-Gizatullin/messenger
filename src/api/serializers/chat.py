from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from core.models import Chat, Message


class ChatSerializer(serializers.ModelSerializer):
    last_message = serializers.SerializerMethodField()

    class Meta:
        model = Chat
        depth = 1
        fields = ['pk', 'users', 'last_message', 'is_dialog']
        extra_kwargs = {'users': {'many': True}}

        validators = [
            UniqueTogetherValidator(
                queryset=Chat.objects.all(),
                fields=['users', 'is_dialog']
            )
        ]

    def get_last_message(self, chat: Chat) -> Message:
        return (
            Message.objects
            .filter(chat=chat.pk)
            .reverse()
            .first())
