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


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ["pk", "author", "chat", "replied_to", "forwarded_by", "text", "created_at", "updated_at"]
