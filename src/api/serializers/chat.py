from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from api.serializers.user import UserSerializer
from core import models
from core.models import Chat, Message, User


class ChatUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['pk']
        extra_kwargs = {'pk': {'read_only': False}}


class ChatSerializer(serializers.ModelSerializer):
    last_message = serializers.SerializerMethodField('get_last_message')
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
        users = attrs.get('users')
        is_dialog = attrs.get('is_dialog')

        if len(users) < 2:
            raise serializers.ValidationError("Impossible to create chat with one or less member")
        elif len(users) > 2 and is_dialog is True:
            raise serializers.ValidationError("Impossible to create chat of dialog type with 2 more users")
        elif is_dialog is True:
            users = [user['pk'] for user in users]
            chat = Chat.objects.all().filter(users__id=users[0]).filter(users__id=users[1])
            if len(chat) != 0:
                raise serializers.ValidationError("chat type of dialog with same members already exists")

        return attrs

    def create(self, validated_data):
        users = validated_data.pop('users')
        chat = Chat.objects.create(**validated_data)
        users = User.objects.all().filter(pk__in=[user["pk"] for user in users])
        chat.users.set(users)
        return chat
