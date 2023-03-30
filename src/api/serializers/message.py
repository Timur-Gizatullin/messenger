from rest_framework import serializers

from core.models import Chat, Message


class MessageCreateSerializer(serializers.ModelSerializer):
    replied_to = serializers.PrimaryKeyRelatedField(queryset=Message.objects.all(), required=False)
    chat_id = serializers.PrimaryKeyRelatedField(queryset=Chat.objects.all(), write_only=True)

    def validate(self, attrs):
        replied_to = attrs.get("replied_to", None)
        text = attrs.get("text", None)
        chat = attrs.pop("chat_id")
        author = self.context["request"].user

        error_message = Chat.objects.validate_before_create(user_id=author.pk, chat_id=chat.pk)

        if error_message:
            raise serializers.ValidationError(error_message)
        if replied_to and replied_to.chat.pk != chat.pk:
            raise serializers.ValidationError("The message is not a part of current chat")

        attrs["author"] = author
        attrs["chat"] = chat
        attrs["text"] = text

        return attrs

    class Meta:
        model = Message
        exclude = [
            "created_at",
            "updated_at",
        ]
        extra_kwargs = {"chat": {"read_only": True}, "author": {"read_only": True}, "forwarded_by": {"read_only": True}}


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = "__all__"
