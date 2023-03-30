from rest_framework import status
from rest_framework.mixins import CreateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from api.serializers.message import MessageCreateSerializer, MessageSerializer
from api.views.mixins import ChatWebSocketDistributorMixin
from core.models import Message
from core.utils.enums import Action


class MessageViewSet(ChatWebSocketDistributorMixin, CreateModelMixin, GenericViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Message.objects.all()

    def get_serializer_class(self):
        if self.action == "create":
            return MessageCreateSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        message = serializer.save()

        self.distribute_to_ws_consumers(dict(serializer.data), Action.CREATE)

        return Response(
            MessageSerializer(instance=message, context={"request": request}).data, status=status.HTTP_201_CREATED
        )
