from rest_framework import serializers

from core.models import Chat, Message


class MessageCreateSerializer(serializers.ModelSerializer):
    replied_to_id = serializers.PrimaryKeyRelatedField(queryset=Message.objects.all(), required=False)

    class Meta:
        model = Message
        fields = ["pk", "chat", "replied_to_id", "text"]

    def validate(self, attrs):
        replied_to = attrs.get("replied_to_id", None)
        chat = attrs["chat"]
        author = self.context["request"].user

        Chat.objects.validate_before_create_message(user_id=author.pk, chat_id=chat.pk)

        if replied_to and replied_to.chat.pk != chat.pk:
            raise serializers.ValidationError("The message is not a part of current chat")

        attrs["author"] = author

        if replied_to:
            attrs["replied_to_id"] = replied_to.pk

        return attrs


class MessageForwardSerializer(serializers.ModelSerializer):
    forward_to_chat_id = serializers.PrimaryKeyRelatedField(queryset=Chat.objects.all(), write_only=True)
    message_ids = serializers.ListSerializer(
        child=serializers.PrimaryKeyRelatedField(queryset=Message.objects.all()), required=True
    )

    class Meta:
        model = Message
        fields = "__all__"
        extra_kwargs = {
            "text": {"read_only": True},
            "author": {"read_only": True},
            "chat": {"read_only": True},
            "replied_to": {"read_only": True},
            "forwarded_by": {"read_only": True},
        }

    def validate(self, attrs):
        user = self.context["request"].user

        if len(attrs["message_ids"]) == 0:
            raise serializers.ValidationError("message_ids field is required")
        if not Message.objects.filter(pk__in=[message.pk for message in attrs["message_ids"]]).filter(
            chat__pk=attrs["message_ids"][0].chat.pk
        ):
            raise serializers.ValidationError("Impossible to forward messages from different chats in one run")

        current_chat_id = Chat.objects.get(messages=attrs["message_ids"][0]).pk
        Chat.objects.validate_before_create_message(user_id=user.pk, chat_id=current_chat_id)
        Chat.objects.validate_before_create_message(user_id=user.pk, chat_id=attrs["forward_to_chat_id"].pk)

        attrs["forwarded_by"] = user

        return attrs

    def create(self, validated_data):
        new_messages = []
        for message in validated_data["message_ids"]:
            new_messages.append(
                Message(
                    forwarded_by=validated_data["forwarded_by"],
                    chat=validated_data["forward_to_chat_id"],
                    author=message.author,
                    replied_to=message.replied_to,
                    text=message.text,
                )
            )

        return Message.objects.bulk_create(new_messages)


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ["pk", "author", "chat", "replied_to", "forwarded_by", "text", "created_at", "updated_at"]
