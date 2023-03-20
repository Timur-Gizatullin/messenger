from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from api.serializers.auth import AuthSignUpSerializer, AuthSignInSerializer
from core.models import User


class AuthViewSet(viewsets.GenericViewSet):
    permission_classes = (AllowAny,)
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.action == "sign_up":
            return AuthSignUpSerializer
        elif self.action == "sign_in":
            return AuthSignInSerializer

    @action(detail=False, methods=['POST'])
    def sign_in(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.save()

        return Response(token, status=status.HTTP_201_CREATED)
