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


class AttachmentForwardSerializer(serializers.ModelSerializer):
    forward_to_chat_id = serializers.PrimaryKeyRelatedField(queryset=Chat.objects.all(), write_only=True)
    attachment_ids = serializers.ListSerializer(
        child=serializers.PrimaryKeyRelatedField(queryset=Attachment.objects.all()), required=True
    )

    class Meta:
        model = Attachment
        fields = "__all__"
        extra_kwargs = {
            "text": {"read_only": True},
            "author": {"read_only": True},
            "chat": {"read_only": True},
            "reply_to_message": {"read_only": True},
            "reply_to_attachment": {"read_only": True},
            "forwarded_by": {"read_only": True},
            "file": {"read_only": True},
        }

    def validate(self, attrs):
        user = self.context["request"].user

        if len(attrs["attachment_ids"]) == 0:
            raise serializers.ValidationError("attachment_ids field is required")
        if not Attachment.objects.filter(pk__in=[message.pk for message in attrs["attachment_ids"]]).filter(
            chat__pk=attrs["attachment_ids"][0].chat.pk
        ):
            raise serializers.ValidationError("Impossible to forward attachments from different chats in one run")

        current_chat_id = Chat.objects.get(attachments=attrs["attachment_ids"][0]).pk
        Chat.objects.validate_before_create_message(user_id=user.pk, chat_id=current_chat_id)
        Chat.objects.validate_before_create_message(user_id=user.pk, chat_id=attrs["forward_to_chat_id"].pk)

        attrs["forwarded_by"] = user

        return attrs

    def create(self, validated_data):
        new_attachments = []
        for attachment in validated_data["attachment_ids"]:
            new_attachments.append(
                Attachment(
                    forwarded_by=validated_data["forwarded_by"],
                    chat=validated_data["forward_to_chat_id"],
                    author=attachment.author,
                    reply_to_message=attachment.reply_to_message,
                    reply_to_attachment=attachment.reply_to_attachment,
                    file=attachment.file,
                    type=attachment.type,
                )
            )

        return Attachment.objects.bulk_create(new_attachments)
