from django.db.models import Q, QuerySet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.parsers import JSONParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from api.serializers.attachment import AttachmentSerializer
from api.views.mixins import (
    ChatWebSocketDistributorMixin,
    UserChatsWebSocketDistributorMixin,
)
from core import constants
from core.models.attachment import Attachment
from core.utils.enums import ActionEnum


class AttachmentViewSet(GenericViewSet):
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.action in ("create", "delete_attachment"):
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

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        ChatWebSocketDistributorMixin.distribute_to_ws_consumers(
            data=dict(serializer.data),
            action=ActionEnum.CREATE,
            postfix=[str(serializer.data["chat"])],
        )

        UserChatsWebSocketDistributorMixin.distribute_to_ws_consumers(
            data=dict(serializer.data),
            action=ActionEnum.CREATE,
            postfix=[str(request.user.pk)],
        )

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["DELETE"])
    def delete_attachment(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        if queryset.count() == 0:
            return Response(data=constants.YOR_ARE_NOT_A_MEMBER_OF_THE_CHAT_OR_AUTHOR, status=status.HTTP_403_FORBIDDEN)

        instance = get_object_or_404(queryset, pk=kwargs["pk"])
        instance.delete()

        ChatWebSocketDistributorMixin.distribute_to_ws_consumers(
            data=dict(self.get_serializer(instance).data),
            action=ActionEnum.DELETE,
            postfix=[str(instance.chat.pk)],
        )

        UserChatsWebSocketDistributorMixin.distribute_to_ws_consumers(
            data=dict(self.get_serializer(instance).data),
            action=ActionEnum.DELETE,
            postfix=[str(request.user.pk)],
        )

        return Response(status=status.HTTP_204_NO_CONTENT)
