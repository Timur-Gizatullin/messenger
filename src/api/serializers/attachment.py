from rest_framework import serializers

from core.models import Chat
from core.models.attachment import Attachment
from core.utils.enums import AttachmentTypeEnum, attachments_type_map


class AttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attachment
        fields = [
            "created_at",
            "updated_at",
            "chat",
            "author",
            "file",
            "type",
            "forwarded_by",
            "reply_to_message",
            "reply_to_attachment",
        ]
        extra_kwargs = {
            "created_at": {"read_only": True},
            "updated_at": {"read_only": True},
            "author": {"read_only": True},
            "type": {"read_only": True},
            "forwarded_by": {"read_only": True},
        }

    def validate(self, attrs):
        reply_to_message = attrs.get("reply_to_message", None)
        reply_to_attachment = attrs.get("reply_to_attachment", None)

        if reply_to_message and reply_to_attachment:
            raise serializers.ValidationError("Choose only one: reply_to_message or reply_to_attachment")

        Chat.objects.validate_before_create_message(user_id=self.context["request"].user.pk, chat_id=attrs["chat"].pk)
        if reply_to_message and not reply_to_message.is_part_of_chat(chat_id=attrs["chat"].pk):
            raise serializers.ValidationError("Chosen message is not part of chat")
        if reply_to_attachment and not reply_to_attachment.is_part_of_chat(chat_id=attrs["chat"].pk):
            raise serializers.ValidationError("Chosen attachment is not part of chat")

        attrs["type"] = attachments_type_map.get(
            self.context["request"].data["file"].content_type, AttachmentTypeEnum.FILE
        )

        attrs["author"] = self.context["request"].user

        return attrs
