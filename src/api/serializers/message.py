from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from core.models import Chat, Message


class MessageCreateSerializer(serializers.ModelSerializer):
    replied_to = serializers.PrimaryKeyRelatedField(queryset=Message.objects.all(), required=False)

    def validate(self, attrs):
        replied_to = attrs.get("replied_to", None)
        text = attrs.get("text", None)
        chat_id = self.context["pk"]
        author = self.context["request"].user

        chat_queryset = Chat.objects.all().filter(pk=chat_id)

        if not chat_queryset.filter(users__id=author.pk):
            raise serializers.ValidationError("Impossible to send message to the chat")
        elif chat_queryset.filter(is_dialog=True).filter(users__is_deleted=True):
            raise serializers.ValidationError("A member is deleted")
        elif text is None or text.strip() == "":
            raise serializers.ValidationError("text or picture should be filled")
        elif replied_to:
            message_replied_to = get_object_or_404(Message, pk=replied_to["pk"])
            attrs["replied_to"] = message_replied_to
            if message_replied_to.chat != chat_id:
                raise serializers.ValidationError("Can not reply to this chat")

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
        extra_kwargs = {
            "chat": {"read_only": True},
            "author": {"read_only": True},
            "forwarded_by": {"read_only": True},
        }


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = "__all__"
