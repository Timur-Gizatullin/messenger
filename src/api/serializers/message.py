from copy import copy

from rest_framework import serializers

from core.models import Message, Chat


class MessageChatSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ["pk"]


class MessageMessageSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ["pk"]
        extra_kwargs = {"pk": {"read_only": True}}


class MessageForwardSerializer(serializers.Serializer):
    forward_to = MessageChatSerializer()
    message_ids = MessageMessageSerializer(many=True)

    class Meta:
        fields = ["forward_to", "message_ids", ]

    def create(self, validated_data):
        new_messages = copy(validated_data["messages"])
        for message in new_messages:
            message.forwarded_by = validated_data["user"]
            message.chat = validated_data["forward_to"]
            message = Message.objects.create(message)
            message.save()

        return new_messages

    def validate(self, attrs):
        user = self.context["request"].user
        message_ids = attrs.pop("message_ids")
        messages = Message.objects.all().filter(id__in=message_ids).get()

        if not Chat.objects.all().filter(pk=attrs["forward_to"]):
            raise serializers.ValidationError("Chat does not exist")
        for message in messages:
            if not Chat.objects.all().filter(pk=message.chat).filter(users=user):
                raise serializers.ValidationError("Can't reach the message")

        attrs["messages"] = messages
        attrs["user"] = user

        return attrs
