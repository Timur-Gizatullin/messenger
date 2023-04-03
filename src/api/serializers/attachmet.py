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

        if not Chat.objects.filter(pk=self.context["pk"]).filter(users=self.context["request"].user):
            raise serializers.ValidationError("User is not a member of the chat")

        attrs["user"] = self.context["request"].user
        attrs["chat"] = chat

        return attrs
