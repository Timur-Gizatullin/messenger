from rest_framework import serializers

from core.models import Chat, Message


class MessageCreateSerializer(serializers.ModelSerializer):
    replied_to = serializers.PrimaryKeyRelatedField(queryset=Message.objects.all(), required=False)

    def validate(self, attrs):
        replied_to = attrs.get("replied_to", None)
        text = attrs.get("text", None)
        chat_id = self.context["pk"]
        author = self.context["request"].user

        chat_queryset = Chat.objects.all().filter(pk=chat_id)
        error_message = Chat.objects.validate_before_create(author.pk, chat_queryset)

        if error_message:
            raise serializers.ValidationError(error_message)
        if replied_to and replied_to.chat.pk != int(chat_id):
            raise serializers.ValidationError("The message is not a part of current chat")

        attrs["author"] = author
        attrs["chat"] = chat_queryset.get()
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
