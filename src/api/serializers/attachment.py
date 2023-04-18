from rest_framework import serializers

from core.models.attachment import Attachment


class AttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attachment
        fields = ["created_at", "updated_at", "chat", "author", "file"]
        extra_kwargs = {
            "created_at": {"read_only": True},
            "updated_at": {"read_only": True},
            "author": {"read_only": True},
            "chat": {"read_only": True},
        }
