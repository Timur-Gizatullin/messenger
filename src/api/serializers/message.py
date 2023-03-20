from rest_framework import serializers

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


class MessageSerializer(serializers.ModelSerializer):
    author = MessageUserSerializer(required=True)
    chat = MessageChatSerializer(required=True)
    replied_to = MessageMessageSerializer(required=False, allow_null=True)
    forwarded_by = MessageUserSerializer(required=False, allow_null=True)
    picture = serializers.ImageField(required=False, allow_null=True)

    def create(self, validated_data):
        text = validated_data["text"]

        message = Message.objects.create(**validated_data)
        message.save()
        return message

    def validate(self, attrs):
        author = attrs['author']["pk"]
        chat = attrs['chat']["pk"]
        replied_to = attrs.get("replied_to", None)
        forwarded_by = attrs.get("forwarded_by", None)
        picture = attrs.get('picture', None)
        text = attrs.get('text', None)

        chat_queryset = Chat.objects.all().filter(pk=chat)
        user_queryset = User.objects.all()
        current_user = self.context["request"].user

        if current_user.is_deleted \
                or ((not forwarded_by and current_user.id != author) or (forwarded_by and current_user.id != forwarded_by["pk"])):
            raise serializers.ValidationError("Impossible to use this account")
        elif not chat_queryset.filter(users__id=author):
            raise serializers.ValidationError("Impossible to send message to the chat")
        elif chat_queryset.filter(is_dialog=True).filter(users__is_deleted=True):
            raise serializers.ValidationError("A member is deleted")
        elif picture is None and text is None:
            raise serializers.ValidationError("text or picture should be filled")
        elif replied_to:
            message_replied_to = Message.objects.get(pk=replied_to["pk"])
            if message_replied_to.chat != chat:
                raise serializers.ValidationError("Can not reply to this chat")

        attrs["author"] = user_queryset.get(pk=author)
        attrs["chat"] = chat_queryset.get()
        if replied_to:
            attrs["replied_to"] = Message.objects.get(pk=replied_to["pk"])
        else:
            attrs["replied_to"] = None
        if forwarded_by:
            attrs["forwarded_by"] = user_queryset.get(pk=forwarded_by["pk"])
        else:
            attrs["forwarded_by"] = None
        attrs["picture"] = picture
        attrs["text"] = text

        return attrs

    def get_group_name(self):
        return f"chat_{self.context['request'].data['chat']['pk']}"

    class Meta:
        model = Message
        exclude = ["created_at", "updated_at", ]
        extra_kwargs = {"text": {"max_length": 255, "allow_null": True, "allow_blank": True}}
