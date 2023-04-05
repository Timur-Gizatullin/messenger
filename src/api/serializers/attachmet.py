from django.shortcuts import get_object_or_404
from rest_framework import serializers

from core.models import Chat
from core.models.attachment import Attachment


class AttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attachment
        fields = ["created_at", "updated_at", "chat", "user", "file"]
        extra_kwargs = {
            "created_at": {"read_only": True},
            "updated_at": {"read_only": True},
            "user": {"read_only": True},
            "chat": {"read_only": True},
        }

    def validate(self, attrs):
        chat = get_object_or_404(Chat, pk=self.context["pk"])

        Chat.objects.validate_before_create_message(user_id=self.context["request"].user.pk, chat_id=chat.pk)

        attrs["user"] = self.context["request"].user
        attrs["chat"] = chat

        return attrs
