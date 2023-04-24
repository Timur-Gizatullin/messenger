from django.db.models import Q, QuerySet
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from api.views.mixins import PaginateMixin
from api.serializers.chat import (
    AddUserToChatInputSerializer,
    ChatCreateSerializer,
    ChatSerializer,
    UserChatSerializer, AddUserToChatOutputSerializer,
)
from api.serializers.attachment import AttachmentSerializer
from api.serializers.message import MessageSerializer
from api.utils import limit, offset
from core import constants
from core.models import Chat, Message, User
from core.models.attachment import Attachment
from core.models.user_chat import UserChat


class ChatViewSet(PaginateMixin, CreateModelMixin, ListModelMixin, GenericViewSet):
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        if self.action in ("get_messages", "delete_message"):
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
        if self.action == "delete_message":
            return (
                super()
                .filter_queryset(queryset)
                .filter(
                    Q(author=self.request.user)
                    | Q(forwarded_by=self.request.user) & Q(chat=self.kwargs["pk"]) & Q(chat__users=self.request.user)
                )
            )

        return super().filter_queryset(queryset)

    def get_serializer_class(self):
        if self.action == "list":
            return ChatSerializer
        if self.action == "create":
            return ChatCreateSerializer
        if self.action == "get_messages":
            return MessageSerializer
        if self.action == "set_user_role":
            return UserChatSerializer
        if self.action == "get_attachments":
            return AttachmentSerializer
        if self.action == "add_user":
            return AddUserToChatInputSerializer

    @swagger_auto_schema(manual_parameters=[limit, offset])
    @action(detail=True, methods=["GET"], url_path="messages")
    def get_messages(self, request, *args, **kwargs):
        return self.get_paginated_queryset(request, *args, **kwargs)

    @action(detail=True, methods=["DELETE"], url_path="messages/(?P<message_id>[0-9]+)")
    def delete_message(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        instance = get_object_or_404(queryset, pk=kwargs["message_id"])
        instance.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

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

        return Response(status=status.HTTP_204_NO_CONTENT)
