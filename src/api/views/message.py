from django.db.models import QuerySet, Q
from rest_framework.mixins import DestroyModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from core.models import Message


class MessageViewSet(DestroyModelMixin, GenericViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Message.objects.all()

    def filter_queryset(self, queryset: QuerySet) -> QuerySet:
        if self.action == "destroy":
            user = self.request.user
            return (
                super().filter_queryset(queryset)
                .filter(Q(author=user) | Q(forwarded_by=user))
            )
        else:
            return super().filter_queryset(queryset)
