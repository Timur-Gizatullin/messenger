from django.db.models import QuerySet, Q
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin
from rest_framework.parsers import JSONParser, MultiPartParser

from api.serializers.attachment import AttachmentSerializer
from core.models.attachment import Attachment


class AttachmentViewSet(CreateModelMixin, GenericViewSet):
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.action == "create":
            return AttachmentSerializer

    def get_queryset(self):
        return Attachment.objects.all()

    def get_parsers(self):
        if self.action_map.get("post", None) and self.action_map["post"] == "create":
            return [
                MultiPartParser(),
            ]

        return [
            JSONParser(),
        ]

    def filter_queryset(self, queryset: QuerySet) -> QuerySet:
        if self.action == "delete_attachment":
            return (
                super().filter_queryset(queryset).filter(Q(chat__users=self.request.user) & Q(author=self.request.user))
            )

        return super().filter_queryset(queryset)

    @action(detail=True, methods=["DELETE"])
    def delete_attachment(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        instance = get_object_or_404(self.get_queryset(), pk=kwargs["pk"])

        if queryset.count() == 0:
            return Response(status=status.HTTP_403_FORBIDDEN)

        instance.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
