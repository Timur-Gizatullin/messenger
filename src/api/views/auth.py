from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from api.serializers.auth import AuthSignUpSerializer, AuthSignInSerializer, AuthUserOutputSerializer
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
    @action(detail=False, methods=['POST'])
    def sign_in(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return Response(
            AuthUserOutputSerializer(instance=user, context={"request": request}).data, status=status.HTTP_200_OK
        )
