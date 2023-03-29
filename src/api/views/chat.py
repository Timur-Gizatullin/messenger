from django.db.models import Q, QuerySet
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from api.serializers.chat import ChatCreateSerializer, ChatSerializer
from api.serializers.message import MessageCreateSerializer, MessageSerializer
from api.views.mixins import ChatWebSocketDistributorMixin
from api.utils import limit, offset
from core.models import Chat, Message
from core.utils.enums import Action



class ChatViewSet(ChatWebSocketDistributorMixin, CreateModelMixin, ListModelMixin, GenericViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Chat.objects.all()

    def get_queryset(self):
        if self.action in ("get_messages", "delete_message"):
            return Message.objects.all()

        return Chat.objects.all()

    def filter_queryset(self, queryset: QuerySet) -> QuerySet:
        if self.action == "list":
            return super().filter_queryset(queryset).filter(users=self.request.user)
        if self.action == "get_messages":
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
        if self.action == "add_message":
            return MessageCreateSerializer

    @swagger_auto_schema(manual_parameters=[limit, offset])
    @action(detail=True, methods=["GET"], url_path="messages")
    def get_messages(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        paginator = LimitOffsetPagination()
        page = paginator.paginate_queryset(queryset, request, view=self)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["DELETE"], url_path="messages/(?P<message_id>[0-9]+)")
    def delete_message(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        instance = get_object_or_404(queryset, pk=kwargs["message_id"])
        instance.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=["POST"])
    def add_message(self, request, pk):
        context = {"request": request, "pk": pk}
        serializer = self.get_serializer(data=request.data, context=context)
        serializer.is_valid(raise_exception=True)
        message = serializer.save()

        self.distribute_to_ws_consumers(serializer.data, Action.CREATE)

        return Response(
            MessageSerializer(instance=message, context={"request": request}).data, status=status.HTTP_201_CREATED
        )
