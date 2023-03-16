from rest_framework import serializers

from core.models import Message, Chat


class MessageSerializer(serializers.ModelSerializer):
    author = serializers.RelatedField()
    chat = serializers.RelatedField()
    replied_to = serializers.RelatedField()
    forwarded_by = serializers.RelatedField()
    picture = serializers.ImageField(allow_null=True, allow_empty_file=True)

    def validate(self, attrs):
        picture = attrs.get('picture', None)
        text = attrs.get('picture', None)
        chat = attrs['chat']
        author = attrs['chat']

        chat_queryset = Chat.objects.all().filter(pk=chat)

        if self.context["request"].user.id != author:
            raise serializers.ValidationError("Impossible to use this account")
        elif not chat_queryset.filter(users__id=author):
            raise serializers.ValidationError("Impossible to send message to the chat")
        elif chat_queryset.filter(is_dialog=True).filter(users__is_deleted=True):
            raise serializers.ValidationError("A member is deleted")
        elif picture is None and text is None:
            raise serializers.ValidationError("text or picture should be filled")

        return attrs

    def get_group_name(self):
        return f"chat_{self.context['request'].data['chat']}"

    class Meta:
        model = Message
        fields = "__all__"
        extra_kwargs = {
            {"text": {
                "max_length": 255,
                "allow_null": True,
                "allow_blank": True}
            },
        }
