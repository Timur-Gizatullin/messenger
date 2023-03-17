from django.db.models import QuerySet
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.settings import api_settings

from api.serializers.user import AuthSignUpSerializer, AuthUserOutputSerializer
from core.models import User


class AuthViewSet(viewsets.GenericViewSet):
    permission_classes = (AllowAny,)
    queryset = User.objects.all()

    @swagger_auto_schema(
        request_body=AuthSignUpSerializer,
        responses={status.HTTP_201_CREATED: AuthUserOutputSerializer()},
        operation_summary="Create new account",
    )
    @action(detail=False, methods=['POST'])
    def sign_up(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.validated_data["email"], status=status.HTTP_201_CREATED)

    def get_serializer_class(self):
        if self.action == "sign_up":
            return AuthSignUpSerializer
