from rest_framework import serializers

from core.models import Chat, Message


class ChatSerializer(serializers.ModelSerializer):
    last_message = serializers.SerializerMethodField()

    class Meta:
        model = Chat
        depth = 1
        fields = ['pk', 'users', 'last_message']
        extra_kwargs = {'users': {'many': True}}

    def get_last_message(self, chat: Chat) -> Message:
        return (
            Message.objects
            .filter(chat=chat.pk)
            .reverse()
            .first())
