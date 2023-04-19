from rest_framework.mixins import CreateModelMixin
from rest_framework.parsers import JSONParser, MultiPartParser
from rest_framework.viewsets import GenericViewSet

from api.serializers.attachment import AttachmentSerializer
from core.models.attachment import Attachment


class AttachmentViewSet(CreateModelMixin, GenericViewSet):
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
