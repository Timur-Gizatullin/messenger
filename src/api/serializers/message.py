from rest_framework import serializers

from core.models import Message


class MessageDeleteSerializer(serializers.Serializer):

    class Meta:
        fields = ["pk"]

    def validate(self, attrs):
        user_id = self.context["request"].user.id
        message = Message.objects.get(pk=attrs["pk"])
        author_pk = message.author.pk
        forward_by = message.forwarded_by

        if (not forward_by and user_id != author_pk) or (forward_by and user_id != forward_by.pk):
            raise serializers.ValidationError("Can't delete message using this account")

        return attrs
