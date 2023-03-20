from django.db.models import QuerySet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.mixins import CreateModelMixin

from api.serializers.chat import ChatSerializer, ChatCreateSerializer
from api.serializers.message import MessageSerializer
from api.views.mixins import ChatWSMixin
from core.models import Chat


class ChatViewSet(ChatWSMixin, CreateModelMixin, ListModelMixin, GenericViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Chat.objects.all()

    def filter_queryset(self, queryset: QuerySet) -> QuerySet:
        if self.action == "list":
            return super().filter_queryset(queryset).filter(users=self.request.user)
        else:
            return super().filter_queryset(queryset)

    def get_serializer_class(self):
        if self.action == "add_message":
            return MessageSerializer
        elif self.action == "list":
            return ChatSerializer
        
    @action(detail=False, methods=["POST"])
    def add_message(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        message = serializer.save()

        ChatWSMixin.send_data_to_ws(self, serializer.data)

        return Response(
                MessageSerializer(instance=message, context={"request": request}).data, status=status.HTTP_201_CREATED
            )
