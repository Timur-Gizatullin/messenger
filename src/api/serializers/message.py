from rest_framework import serializers

from core.models import Chat, Message


class MessageForwardSerializer(serializers.ModelSerializer):
    forward_to_id = serializers.PrimaryKeyRelatedField(queryset=Chat.objects.all(), write_only=True)
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

    def create(self, validated_data):
        messages = validated_data["messages"]
        new_messages = []
        for message in messages:
            new_message = {
                "forwarded_by": validated_data["user"],
                "chat": validated_data["forward_to"],
                "author": message.author,
                "replied_to": message.replied_to,
                "text": message.text,
            }
            new_messages.append(Message.objects.create(**new_message))

        return new_messages

    def validate(self, attrs):
        user = self.context["request"].user
        messages = attrs.pop("message_ids")
        forward_to = attrs.pop("forward_to_id")
        if not forward_to.users.contains(user):
            raise serializers.ValidationError("User is not a member of the chat to forward")
        for message in messages:
            if not Chat.objects.all().filter(pk=message.chat.pk).filter(users=user):
                raise serializers.ValidationError("User is not a member of the current chat")

        attrs["messages"] = messages
        attrs["user"] = user
        attrs["forward_to"] = forward_to

        return attrs


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = "__all__"
