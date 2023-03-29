from copy import copy

from django.db.models import Q
from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from core.models import Chat, Message


class MessagePrimaryKeyRelatedField(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ["pk"]
        extra_kwargs = {"pk": {"read_only": False}}


class MessageForwardSerializer(serializers.ModelSerializer):
    forward_to = serializers.PrimaryKeyRelatedField(queryset=Chat.objects.all(), write_only=True)
    message_ids = MessagePrimaryKeyRelatedField(many=True)

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
        new_messages = copy(validated_data["messages"])

        for message in new_messages:
            message.forwarded_by = validated_data["user"]
            message.chat = validated_data["forward_to"]
            message.pk = None
            message.save()

        return new_messages

    def validate(self, attrs):
        user = self.context["request"].user
        message_ids = [message["pk"] for message in attrs.pop("message_ids")]
        messages = Message.objects.all().filter(id__in=message_ids)
        forward_to = attrs["forward_to"]
        if not forward_to.users.contains(user):
            raise serializers.ValidationError("Can't reach the chat to forward")
        for message in messages:
            if not Chat.objects.all().filter(pk=message.chat.pk).filter(users=user):
                raise serializers.ValidationError("Can't reach the message")

        attrs["messages"] = messages
        attrs["user"] = user

        return attrs


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = "__all__"
