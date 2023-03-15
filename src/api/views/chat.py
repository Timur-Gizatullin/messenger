from django.db.models import QuerySet
from rest_framework import viewsets
from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.mixins import CreateModelMixin

from api.serializers import ChatSerializer
from core.models import Chat


class ChatViewSet(CreateModelMixin, ListModelMixin, viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer

    def filter_queryset(self, queryset: QuerySet) -> QuerySet:
        if self.action == "list":
            return super().filter_queryset(queryset).filter(users=self.request.user)
        elif self.action == 'create':
            return (
                super().filter_queryset(queryset)
                .filter(users__cantains=[self.request.user.pk, self.request.data.get('user_id')])
                .filter(is_dialog=True))
