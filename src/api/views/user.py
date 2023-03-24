from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet


class UserViewSet(GenericViewSet):
    @action(detail=False, methods=["PATCH"])
    def upload_profile_picture(self, request, *args, **kwargs):
        picture = request.data["image"]
        user = request.user
        user.profile_picture = picture
        user.save()

        return Response({"message": "picture uploaded"}, status=status.HTTP_200_OK)
