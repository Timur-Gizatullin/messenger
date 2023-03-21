from django.db.models import QuerySet
from rest_framework.mixins import DestroyModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from api.serializers.message import MessageDeleteSerializer
from core.models import Chat


class MessageViewSet(DestroyModelMixin, GenericViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Chat.objects.all()

    def filter_queryset(self, queryset: QuerySet) -> QuerySet:
        if self.action == "destroy":
            return super().filter_queryset(queryset).filter(author=self.request.user)
        else:
            return super().filter_queryset(queryset)

    def get_serializer_class(self):
        if self.action == 'destroy':
            return MessageDeleteSerializer
