from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from api.serializers.auth import (
    AuthSignInSerializer,
    AuthSignUpSerializer,
    AuthUserOutputSerializer,
)
from core.models import User


class AuthViewSet(viewsets.GenericViewSet):
    permission_classes = (AllowAny,)
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.action == "sign_up":
            return AuthSignUpSerializer
        elif self.action == "sign_in":
            return AuthSignInSerializer

    @swagger_auto_schema(
        request_body=AuthSignInSerializer,
        responses={status.HTTP_200_OK: AuthUserOutputSerializer()},
    )
    @action(detail=False, methods=["POST"])
    def sign_in(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return Response(
            AuthUserOutputSerializer(instance=user, context={"request": request}).data, status=status.HTTP_200_OK
        )

    @swagger_auto_schema(
        request_body=AuthSignUpSerializer,
        responses={status.HTTP_201_CREATED: AuthUserOutputSerializer()},
        operation_summary="Create new account",
    )
    @action(detail=False, methods=["POST"])
    def sign_up(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return Response(
            AuthUserOutputSerializer(instance=user, context={"request": request}).data, status=status.HTTP_201_CREATED
        )
