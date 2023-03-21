from rest_framework.mixins import CreateModelMixin
from rest_framework.viewsets import GenericViewSet

from api.serializers.message import MessageForwardSerializer


class MessageViewSet(CreateModelMixin, GenericViewSet):
    def get_serializer_class(self):
        if self.action == "create":
            return MessageForwardSerializer
