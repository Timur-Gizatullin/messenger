from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from api.serializers.message import (
    MessageCreateSerializer,
    MessageForwardSerializer,
    MessageSerializer,
)
from api.views.mixins import (
    ChatWebSocketDistributorMixin,
    UserChatsWebSocketDistributorMixin,
)
from core.models import Message
from core.utils.enums import ActionEnum, WSType


class MessageViewSet(GenericViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Message.objects.all()

    def get_serializer_class(self):
        if self.action in ("create", "delete_message"):
            return MessageCreateSerializer
        if self.action == "forward":
            return MessageForwardSerializer

    def filter_queryset(self, queryset):
        if self.action == "delete_message":
            return (
                super()
                .filter_queryset(queryset)
                .filter(
                    Q(chat__users=self.request.user) & Q(author=self.request.user) | Q(forwarded_by=self.request.user)
                )
                .distinct()
            )

        return super().filter_queryset(queryset)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        message = serializer.save()

        ChatWebSocketDistributorMixin.distribute_to_ws_consumers(
            data=dict(serializer.data),
            action=ActionEnum.CREATE,
            postfix=[str(message.chat.pk)],
            ws_type=WSType.CHAT_MESSAGE,
        )

        UserChatsWebSocketDistributorMixin.distribute_to_ws_consumers(
            data=dict(serializer.data),
            action=ActionEnum.CREATE,
            postfix=[str(request.user.pk)],
            ws_type=WSType.CHAT_CHATS,
        )

        return Response(
            MessageSerializer(instance=message, context={"request": request}).data, status=status.HTTP_201_CREATED
        )

    @action(detail=False, methods=["POST"], url_path="forward")
    def forward(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        new_messages = serializer.save()

        ws_response = {
            "new_messages": [dict(new_message) for new_message in MessageSerializer(new_messages, many=True).data]
        }

        ChatWebSocketDistributorMixin.distribute_to_ws_consumers(
            data=ws_response,
            action=ActionEnum.CREATE,
            postfix=[str(request.data["forward_to_chat_id"])],
            ws_type=WSType.CHAT_MESSAGE,
        )

        UserChatsWebSocketDistributorMixin.distribute_to_ws_consumers(
            data=ws_response,
            action=ActionEnum.CREATE,
            postfix=[str(request.user.pk)],
            ws_type=WSType.CHAT_CHATS,
        )

        return Response(MessageSerializer(new_messages, many=True).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["DELETE"])
    def delete_message(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        instance = get_object_or_404(queryset, pk=kwargs["pk"])
        instance.delete()

        ChatWebSocketDistributorMixin.distribute_to_ws_consumers(
            data=dict(self.get_serializer(instance).data),
            action=ActionEnum.DELETE,
            postfix=[str(instance.chat.pk)],
            ws_type=WSType.CHAT_MESSAGE,
        )

        UserChatsWebSocketDistributorMixin.distribute_to_ws_consumers(
            data=dict(self.get_serializer(instance).data),
            action=ActionEnum.DELETE,
            postfix=[str(request.user.pk)],
            ws_type=WSType.CHAT_CHATS,
        )

        return Response(status=status.HTTP_204_NO_CONTENT)
