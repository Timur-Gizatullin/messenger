from rest_framework import serializers

from core.models import Message


class MessageSerializer(serializers.ModelSerializer):
    def validate(self, data):
        if data["text"] is None or data["text"].replace(" ", "") == "" or data["picture"] is None:
            raise serializers.ValidationError("Missing required args")

    class Meta:
        model = Message
        fields = "__all__"
        depth = 1
