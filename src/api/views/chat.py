from django.db.models import QuerySet
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated

from rest_framework.viewsets import GenericViewSet

from api.serializers.chat import ChatCreateSerializer, ChatSerializer
from api.serializers.message import MessageSerializer
from core.models import Chat, Message


class ChatViewSet(CreateModelMixin, ListModelMixin, GenericViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Chat.objects.all()
    pagination_class = LimitOffsetPagination

    limit = openapi.Parameter('limit', openapi.IN_QUERY, description="Number of results to return per page.", type=openapi.TYPE_INTEGER)
    offset = openapi.Parameter('offset', openapi.IN_QUERY, description="The initial index from which to return the results.", type=openapi.TYPE_INTEGER)

    @swagger_auto_schema(manual_parameters=[limit, offset])
    @action(detail=True, methods=["GET"], url_path="messages")
    def get_messages(self, request, pk):
        return self.list(request)

    def get_queryset(self):
        if self.action == "get_messages":
            return Message.objects.all()
        else:
            return Chat.objects.all()

    def filter_queryset(self, queryset: QuerySet) -> QuerySet:
        if self.action == "list":
            return super().filter_queryset(queryset).filter(users=self.request.user)
        elif self.action == "get_messages":
            return super().filter_queryset(queryset).filter(chat=self.kwargs["pk"])
        else:
            return super().filter_queryset(queryset)

    def get_serializer_class(self):
        if self.action == "list":
            return ChatSerializer
        elif self.action == "create":
            return ChatCreateSerializer
        elif self.action == "get_messages":
            return MessageSerializer
