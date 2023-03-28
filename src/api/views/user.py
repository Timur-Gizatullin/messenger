from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.parsers import MultiPartParser, JSONParser

from api.serializers.user import UploadProfilePicSerializer
from core.models import User


class UserViewSet(GenericViewSet):
    permission_classes = (IsAuthenticated, )
    queryset = User.objects.all()

    def get_parsers(self):
        if self.action_map["post"] == "upload_profile_picture":
            return [MultiPartParser(), ]

        return [JSONParser(), ]

    def get_serializer_class(self):
        if self.action == "upload_profile_picture":
            return UploadProfilePicSerializer

    @action(detail=False, methods=["POST"])
    def upload_profile_picture(self, request, *args, **kwargs):
        picture = request.FILES

        serializer = self.get_serializer(data=picture)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_204_NO_CONTENT)
