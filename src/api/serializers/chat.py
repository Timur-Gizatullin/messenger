from rest_framework import serializers

from core.models import Chat, Message, User


class ChatUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['pk']
        extra_kwargs = {'pk': {'read_only': False}}


class ChatSerializer(serializers.ModelSerializer):
    last_message = serializers.SerializerMethodField()
    users = ChatUserSerializer(many=True)

    class Meta:
        model = Chat
        fields = ['pk', 'users', 'last_message', 'is_dialog']

    def get_last_message(self, chat: Chat) -> Message:
        return (
            Message.objects
            .filter(chat=chat.pk)
            .reverse()
            .first())


class ChatCreateSerializer(ChatSerializer):
    users = ChatUserSerializer(many=True)

    def validate(self, attrs):
        users = attrs['users']
        users = [user['pk'] for user in users]
        is_dialog = attrs['is_dialog']
        request = self.context.get('request', None)
        users_count = len(users)

        if request is not None and users.__contains__(request.user.id):
            raise serializers.ValidationError("Impossible create chat without current user as member")
        elif users_count < 2:
            raise serializers.ValidationError("Impossible to create chat with one or less member")
        elif users_count > 2 and is_dialog is True:
            raise serializers.ValidationError("Impossible to create chat of dialog type with 2 more users")
        elif is_dialog is True:
            chat = Chat.objects.all().filter(users__id=users[0]).filter(users__id=users[1])
            if len(chat) != 0:
                raise serializers.ValidationError("chat type of dialog with same members already exists")

        return attrs

    def create(self, validated_data):
        validated_users = validated_data.pop('users')
        chat = Chat.objects.create(**validated_data)
        users_queryset = User.objects.all().filter(pk__in=validated_users)
        chat.users.set(users_queryset)
        return chat
