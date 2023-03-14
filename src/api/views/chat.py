from django.db.models import QuerySet
from rest_framework import viewsets, status
from rest_framework.mixins import CreateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.serializers import ChatSerializer
from core.models import Chat


class ChatViewSet(CreateModelMixin, viewsets.GenericViewSet):
    permission_classes = IsAuthenticated

    def filter_queryset(self, queryset: QuerySet) -> QuerySet:
        if self.action == 'create':
            return (
                super().filter_queryset(queryset)
                .filter(users__cantains=[self.request.user.pk, self.request.data.get('user_id')])
                .filter(is_dialog=True))
        elif self.action == 'list':
            return super().filter_queryset(queryset).filter(user=self.request.user)
