from django.db.models import QuerySet
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import IsAuthenticated, AllowAny

from api.serializers import ChatSerializer
from api.serializers.message import MessageSerializer
from core.models import Chat


class ChatViewSet(ListModelMixin, viewsets.GenericViewSet):
    permission_classes = (AllowAny,)
    queryset = Chat.objects.all()

    @action(detail=False, methods=["POST"])
    def add_message(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        message = serializer.save()

        return Response(
            MessageSerializer(instance=message, context={"request": request}).data, status=status.HTTP_201_CREATED
        )

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
