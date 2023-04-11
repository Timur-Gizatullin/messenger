from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from api.serializers.message import MessageSerializer
from core.models import Chat, Message, User
from core.models.user_chat import UserChat
from core.utils.enums import ChatRoleEnum


class ChatUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["pk"]
        extra_kwargs = {"pk": {"read_only": False}}


class ChatSerializer(serializers.ModelSerializer):
    last_message = serializers.SerializerMethodField()
    users = ChatUserSerializer(many=True)

    class Meta:
        model = Chat
        depth = 1
        fields = ["pk", "users", "last_message", "is_dialog"]
        extra_kwargs = {"users": {"many": True}}

    def get_last_message(self, chat: Chat) -> Message:
        message = Message.objects.filter(chat=chat.pk).reverse().first()
        if message:
            message = MessageSerializer(message)
            return message.data
        return message


class ChatCreateSerializer(ChatSerializer):
    users = ChatUserSerializer(many=True)

    def validate(self, attrs):
        users = attrs["users"]
        users = [user["pk"] for user in users]
        is_dialog = attrs["is_dialog"]
        request = self.context["request"]
        users_count = len(users)

        if request.user and not users.__contains__(request.user.id):
            raise serializers.ValidationError("Impossible create chat without current user as member")
        elif users_count < 2:
            raise serializers.ValidationError("Impossible to create chat with one or less member")
        elif users_count > 2 and is_dialog is True:
            raise serializers.ValidationError("Impossible to create chat of dialog type with 2 more users")
        elif is_dialog is True:
            chat = Chat.objects.all().filter(users__id=users[0]).filter(users__id=users[1])
            if len(chat) != 0:
                raise serializers.ValidationError("chat type of dialog with same members already exists")

        attrs["users"] = users
        return attrs

    def create(self, validated_data):
        validated_users = validated_data.pop("users")
        chat = Chat.objects.create(**validated_data)
        users_queryset = User.objects.all().filter(pk__in=validated_users)
        chat.users.set(users_queryset)
        chat.save()
        user_chat = UserChat.objects.filter(user=self.context["request"].user).filter(chat=chat).get()
        user_chat.role = ChatRoleEnum.OWNER
        user_chat.save()

        return chat


class UserChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserChat
        fields = ["user", "chat", "role"]
        extra_kwargs = {"user": {"read_only": True}, "chat": {"read_only": True}}

    def validate(self, attrs):
        user_chat_to_update = get_object_or_404(
            UserChat, Q(chat__id=self.context["pk"]) & Q(user=self.context["user_id"])
        )
        current_user_chat = get_object_or_404(
            UserChat, Q(chat__id=self.context["pk"]) & Q(user=self.context["request"].user)
        )

        if not (current_user_chat.role == ChatRoleEnum.OWNER or current_user_chat.role == ChatRoleEnum.ADMIN):
            raise serializers.ValidationError(f"{current_user_chat.role} role doesnt allow update user roles")
        if user_chat_to_update.role == ChatRoleEnum.OWNER:
            raise serializers.ValidationError("Impossible to update owner role")
        if attrs["role"] == ChatRoleEnum.OWNER:
            raise serializers.ValidationError("OWNER is not allowed as choice")

        attrs["user_chat_to_update"] = user_chat_to_update

        return attrs

    def create(self, validated_data):
        user_chat_to_update = validated_data["user_chat_to_update"]
        user_chat_to_update.role = validated_data["role"]
        user_chat_to_update.save()

        return user_chat_to_update
