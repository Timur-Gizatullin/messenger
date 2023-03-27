from django.db.models import QuerySet
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from api.serializers.chat import ChatCreateSerializer, ChatSerializer
from api.serializers.message import MessageSerializer, MessageCreateSerializer
from api.views.mixins import ChatWSMixin
from core.models import Chat, Message

limit = openapi.Parameter(
    "limit", openapi.IN_QUERY, description="Number of results to return per page.", type=openapi.TYPE_INTEGER
)
offset = openapi.Parameter(
    "offset",
    openapi.IN_QUERY,
    description="The initial index from which to return the results.",
    type=openapi.TYPE_INTEGER,
)


class ChatViewSet(ChatWSMixin, CreateModelMixin, ListModelMixin, GenericViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Chat.objects.all()

    def get_queryset(self):
        if self.action == "get_messages":
            return Message.objects.all()

        return Chat.objects.all()

    def filter_queryset(self, queryset: QuerySet) -> QuerySet:
        if self.action == "list":
            return super().filter_queryset(queryset).filter(users=self.request.user)
        if self.action == "get_messages":
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
        
    @action(detail=True, methods=["POST"])
    def add_message(self, request, pk):
        request.data["chat"] = pk
        request.data["author"] = request.user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        message = serializer.save()

        ChatWSMixin.send_data_to_ws(self, serializer.data)

        return Response(
                MessageSerializer(instance=message, context={"request": request}).data, status=status.HTTP_201_CREATED
            )
