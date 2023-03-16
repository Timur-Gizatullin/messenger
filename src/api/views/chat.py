from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db.models import QuerySet
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import IsAuthenticated

from api.serializers import ChatSerializer
from api.serializers.message import MessageSerializer
from core.models import Chat


class ChatViewSet(ListModelMixin, viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer()

    @action(detail=False, methods=["post"])
    def add_message(self, request):
        message = request["message"]
        serializer = MessageSerializer(message)
        serializer.save()

        return Response(message, status=status.HTTP_201_CREATED)

    def filter_queryset(self, queryset: QuerySet) -> QuerySet:
        if self.action == "list":
            return super().filter_queryset(queryset).filter(users=self.request.user)
