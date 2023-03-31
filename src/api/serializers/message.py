from rest_framework import serializers

from core.models import Chat, Message


class MessageForwardSerializer(serializers.ModelSerializer):
    forward_to_chat_id = serializers.PrimaryKeyRelatedField(queryset=Chat.objects.all(), write_only=True)
    message_ids = serializers.ListSerializer(child=serializers.PrimaryKeyRelatedField(queryset=Message.objects.all()))

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

        if not attrs["forward_to_chat_id"].users.contains(user):
            raise serializers.ValidationError("User is not a member of the chat to forward")
        for message in attrs["message_ids"]:
            if not Chat.objects.all().filter(pk=message.chat.pk).filter(users=user):
                raise serializers.ValidationError("User is not a member of the current chat")

        attrs["forwarded_by"] = user

        return attrs

    def create(self, validated_data):
        new_messages = []
        for message in validated_data["message_ids"]:
            new_message = {
                "forwarded_by": validated_data["forwarded_by"],
                "chat": validated_data["forward_to_chat_id"],
                "author": message.author,
                "replied_to": message.replied_to,
                "text": message.text,
            }
            new_messages.append(Message.objects.create(**new_message))

        return new_messages


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = "__all__"
