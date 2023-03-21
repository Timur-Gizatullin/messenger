from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet


class ChatViewSet(GenericViewSet):

    @action(detail=False, methods=["POST"])
    def upload_profile_picture(self, request):
        picture = request.data["file"]
        user = request.user
        user.profile_picture = picture
        user.save()

        return Response({"message": "picture uploaded"}, status=status.HTTP_200_OK)
