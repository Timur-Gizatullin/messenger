from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from api.serializers.message import MessageForwardSerializer, MessageSerializer
from core.models import Message


class MessageViewSet(GenericViewSet):
    queryset = Message.objects.all()

    def get_serializer_class(self):
        if self.action == "forward":
            return MessageForwardSerializer

    @action(detail=False, methods=["POST"], url_path="forward")
    def forward(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        new_messages = serializer.save()

        return Response(MessageSerializer(new_messages, many=True).data, status=status.HTTP_201_CREATED)
