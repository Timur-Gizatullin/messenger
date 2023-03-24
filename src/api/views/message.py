from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin
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

        messages_response = MessageSerializer(data=new_messages, many=True)
        messages_response.is_valid()

        return Response(messages_response.data, status=status.HTTP_201_CREATED)
