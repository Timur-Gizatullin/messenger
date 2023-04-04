from rest_framework import serializers

from core.models import Chat, Message


class MessageForwardSerializer(serializers.ModelSerializer):
    forward_to_chat_id = serializers.PrimaryKeyRelatedField(queryset=Chat.objects.all(), write_only=True)
    message_ids = serializers.ListSerializer(child=serializers.PrimaryKeyRelatedField(queryset=Message.objects.all()),
                                             required=True)

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

        current_chat_id = Chat.objects.get(messages=attrs["message_ids"][0]).pk
        Chat.objects.validate_before_create_message(user_id=user.pk, chat_id=current_chat_id)

        if not Chat.objects.filter(pk=attrs["forward_to_chat_id"].pk).filter(users__id=user.pk):
            raise serializers.ValidationError("User is not a member of the chat to forward")
        if (not Message.objects
                .filter(pk__in=[message.pk for message in attrs["message_ids"]])
                .filter(chat__pk=attrs["message_ids"][0].chat.pk)):
            raise serializers.ValidationError("Impossible to forward messages from different chats in one run")

        attrs["forwarded_by"] = user

        return attrs

    def create(self, validated_data):
        new_messages = []
        for message in validated_data["message_ids"]:
            new_messages.append(Message(
                forwarded_by=validated_data["forwarded_by"],
                chat=validated_data["forward_to_chat_id"],
                author=message.author,
                replied_to=message.replied_to,
                text=message.text
            ))

        return Message.objects.bulk_create(new_messages)


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = "__all__"
