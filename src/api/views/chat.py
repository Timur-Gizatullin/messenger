from django.db.models import QuerySet
from rest_framework import viewsets
from rest_framework.authentication import BasicAuthentication
from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import IsAuthenticated

from api.serializers import ChatSerializer
from core.models import Chat


class ChatViewSet(ListModelMixin, viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer

    def filter_queryset(self, queryset: QuerySet) -> QuerySet:
        if self.action == "list":
            return super().filter_queryset(queryset).filter(users=self.request.user)
