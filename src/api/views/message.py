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
from api.views.mixins import ChatWebSocketDistributorMixin
from core.models import Message
from core.utils.enums import Action


class MessageViewSet(ChatWebSocketDistributorMixin, GenericViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Message.objects.all()

    def get_serializer_class(self):
        if self.action == "create":
            return MessageCreateSerializer
        if self.action == "forward":
            return MessageForwardSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        message = serializer.save()

        self.distribute_to_ws_consumers(
            data=dict(serializer.data), action=Action.CREATE, postfix=[str(message.chat.pk)]
        )

        return Response(
            MessageSerializer(instance=message, context={"request": request}).data, status=status.HTTP_201_CREATED
        )

    @action(detail=False, methods=["POST"], url_path="forward")
    def forward(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        new_messages = serializer.save()

        return Response(MessageSerializer(new_messages, many=True).data, status=status.HTTP_201_CREATED)
