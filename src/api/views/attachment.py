from django.db.models import Q, QuerySet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from core.models.attachment import Attachment


class AttachmentViewSet(GenericViewSet):
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        if self.action == "delete_attachment":
            return Attachment.objects.all()

    def filter_queryset(self, queryset: QuerySet) -> QuerySet:
        if self.action == "delete_attachment":
            return (
                super().filter_queryset(queryset).filter(Q(chat__users=self.request.user) & Q(user=self.request.user))
            )

        return super().filter_queryset(queryset)

    @action(detail=True, methods=["DELETE"])
    def delete_attachment(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        if queryset.count() == 0:
            return Response(status=status.HTTP_403_FORBIDDEN)

        instance = get_object_or_404(queryset, pk=kwargs["pk"])
        instance.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
