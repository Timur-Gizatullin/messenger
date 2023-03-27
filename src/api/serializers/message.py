from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from core.models import Message, Chat, User


class MessageUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['pk']
        extra_kwargs = {'pk': {'read_only': False}}


class MessageChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = ['pk']
        extra_kwargs = {'pk': {'read_only': False}}


class MessageMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['pk']
        extra_kwargs = {'pk': {'read_only': False}}


class MessageCreateSerializer(serializers.ModelSerializer):
    replied_to = MessageMessageSerializer(required=False, allow_null=True)
    picture = serializers.ImageField(required=False, allow_null=True)

    def create(self, validated_data):
        message = Message.objects.create(**validated_data)
        message.save()
        return message

    def validate(self, attrs):
        replied_to = attrs.get("replied_to", None)
        picture = attrs.get('picture', None)
        text = attrs.get('text', None)
        chat_id = self.initial_data["chat"]
        author = self.initial_data["author"]

        chat_queryset = Chat.objects.all().filter(pk=chat_id)

        if not chat_queryset.filter(users__id=author.pk):
            raise serializers.ValidationError("Impossible to send message to the chat")
        elif chat_queryset.filter(is_dialog=True).filter(users__is_deleted=True):
            raise serializers.ValidationError("A member is deleted")
        elif picture is None and (text is None or text.strip() == ""):
            raise serializers.ValidationError("text or picture should be filled")
        elif replied_to:
            message_replied_to = get_object_or_404(Message, pk=replied_to["pk"])
            attrs["replied_to"] = message_replied_to
            if message_replied_to.chat != chat_id:
                raise serializers.ValidationError("Can not reply to this chat")

        attrs["author"] = author
        attrs["chat"] = chat_queryset.get()
        attrs["picture"] = picture
        attrs["text"] = text

        return attrs

    class Meta:
        model = Message
        exclude = ["created_at", "updated_at", ]
        extra_kwargs = {
            "text": {"max_length": 255, "allow_null": True, "allow_blank": True},
            "chat": {"read_only": True},
            "author": {"read_only": True},
            "forwarded_by": {"read_only": True}
        }


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = "__all__"
