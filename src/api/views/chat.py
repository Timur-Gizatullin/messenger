from django.db.models import QuerySet
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from api.serializers.attachment import AttachmentSerializer
from api.serializers.chat import (
    AddUserToChatInputSerializer,
    AddUserToChatOutputSerializer,
    ChatCreateSerializer,
    ChatSerializer,
    UserChatSerializer,
)
from api.serializers.message import MessageSerializer
from api.utils import limit, offset
from api.views.mixins import (
    ChatWebSocketDistributorMixin,
    PaginateMixin,
    UserChatsWebSocketDistributorMixin,
)
from core import constants
from core.models import Chat, Message, User
from core.models.attachment import Attachment
from core.models.user_chat import UserChat
from core.utils.enums import ActionEnum


class ChatViewSet(ChatWebSocketDistributorMixin, PaginateMixin, CreateModelMixin, ListModelMixin, GenericViewSet):
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        if self.action == "get_messages":
            return Message.objects.all()
        if self.action == "get_attachments":
            return Attachment.objects.all()
        if self.action == "delete_user":
            return User.objects.all()

        return Chat.objects.all()

    def filter_queryset(self, queryset: QuerySet) -> QuerySet:
        if self.action == "list":
            return super().filter_queryset(queryset).filter(users=self.request.user)
        if self.action in ("get_messages", "get_attachments"):
            return (
                super().filter_queryset(queryset).filter(chat__users=self.request.user).filter(chat=self.kwargs["pk"])
            )

        return super().filter_queryset(queryset)

    def get_serializer_class(self):
        if self.action == "list":
            return ChatSerializer
        if self.action == "create":
            return ChatCreateSerializer
        if self.action == "get_messages":
            return MessageSerializer
        if self.action in ("set_user_role", "delete_user"):
            return UserChatSerializer
        if self.action == "get_attachments":
            return AttachmentSerializer
        if self.action == "add_user":
            return AddUserToChatInputSerializer

    @swagger_auto_schema(manual_parameters=[limit, offset])
    @action(detail=True, methods=["GET"], url_path="messages")
    def get_messages(self, request, *args, **kwargs):
        return self.get_paginated_queryset(request, *args, **kwargs)

    @action(detail=True, methods=["PATCH"], url_path="users/(?P<user_id>[0-9]+)/role")
    def set_user_role(self, request, *args, **kwargs):
        context = {"request": request, "chat_id": kwargs["pk"], "user_to_update_id": kwargs["user_id"]}

        serializer = self.get_serializer(data=request.data, context=context)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["POST"], url_path="users")
    def add_user(self, request, *args, **kwargs):
        context = {"request": request, "chat_id": kwargs["pk"]}

        serializer = self.get_serializer(data=request.data, context=context)
        serializer.is_valid(raise_exception=True)
        new_users = serializer.save()

        ws_response = {
            "new_chat_users": [
                dict(new_message) for new_message in AddUserToChatOutputSerializer(new_users, many=True).data
            ]
        }

        UserChatsWebSocketDistributorMixin.distribute_to_ws_consumers(
            data=ws_response,
            action=ActionEnum.CREATE,
            postfix=[str(request.user.pk)],
        )

        return Response(AddUserToChatOutputSerializer(new_users, many=True).data, status=status.HTTP_200_OK)

    @swagger_auto_schema(manual_parameters=[limit, offset])
    @action(detail=True, methods=["GET"])
    def get_attachments(self, request, *args, **kwargs):
        return self.get_paginated_queryset(request, *args, **kwargs)

    @action(detail=True, methods=["DELETE"], url_path="users/(?P<user_id>[0-9]+)")
    def delete_user(self, request, *args, **kwargs):
        user_chat_to_delete = get_object_or_404(UserChat, user__id=kwargs["user_id"], chat__id=kwargs["pk"])

        if user_chat_to_delete.is_chat_owner():
            return Response(data=constants.YOU_CANNOT_DELETE_CHAT_OWNER, status=status.HTTP_403_FORBIDDEN)
        if not get_object_or_404(UserChat, user=request.user, chat__id=kwargs["pk"]).can_add_or_delete_user_from_chat():
            return Response(data=constants.YOU_HAVE_NO_PERMISSION_TO_DELETE_USER, status=status.HTTP_403_FORBIDDEN)

        user_chat_to_delete.delete()

        UserChatsWebSocketDistributorMixin.distribute_to_ws_consumers(
            data=dict(self.get_serializer(user_chat_to_delete).data),
            action=ActionEnum.DELETE,
            postfix=[str(request.user.pk)],
        )

        return Response(status=status.HTTP_204_NO_CONTENT)
