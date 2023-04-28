from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied

from api.serializers.image import StdImageSerializer
from api.serializers.message import MessageSerializer
from core import constants
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
            UserChat, Q(chat__id=self.context["chat_id"]) & Q(user=self.context["user_to_update_id"])
        )
        current_user_chat = get_object_or_404(
            UserChat, Q(chat__id=self.context["chat_id"]) & Q(user=self.context["request"].user)
        )

        if not current_user_chat.can_update_roles():
            raise serializers.ValidationError(constants.YOU_CANNOT_SET_THE_ROLE_OF_OTHERS_USERS_OF_THIS_CHAT)
        if user_chat_to_update.is_chat_owner():
            raise serializers.ValidationError(constants.OWNER_ROLE_IS_IMMUTABLE)
        if attrs["role"] == ChatRoleEnum.OWNER:
            raise serializers.ValidationError(constants.OWNER_IS_NOT_ALLOWED_AS_CHOICE)

        attrs["user_chat_to_update"] = user_chat_to_update

        return attrs

    def create(self, validated_data):
        user_chat_to_update = validated_data["user_chat_to_update"]
        user_chat_to_update.role = validated_data["role"]
        user_chat_to_update.save()

        return user_chat_to_update


class AddUserToChatInputSerializer(serializers.ModelSerializer):
    user_ids = serializers.ListSerializer(
        child=serializers.PrimaryKeyRelatedField(queryset=User.objects.all()),
        required=True,
        write_only=True,
    )

    class Meta:
        model = User
        fields = [
            "pk",
            "user_ids",
        ]

    def validate(self, attrs):
        attrs["chat"] = get_object_or_404(
            Chat, pk=self.context["chat_id"], users=self.context["request"].user, is_dialog=False
        )

        user_chat = UserChat.objects.get(chat=self.context["chat_id"], user=self.context["request"].user.pk)

        if not user_chat.can_add_or_delete_user_from_chat():
            raise PermissionDenied(constants.ONLY_ADMIN_OR_OWNER_CAN_ADD_USERS_TO_CHAT)

        return attrs

    def create(self, validated_data):
        for new_user in validated_data["user_ids"]:
            validated_data["chat"].users.add(new_user)
        return validated_data["user_ids"]


class AddUserToChatOutputSerializer(serializers.ModelSerializer):
    profile_picture = StdImageSerializer(read_only=True)

    class Meta:
        model = User
        fields = [
            "pk",
            "email",
            "profile_picture",
        ]
        extra_kwargs = {"email": {"read_only": True}}
