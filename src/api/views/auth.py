from django.db.models import QuerySet
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from api.serializers.user import UserSerializer
from core.models import User


class AuthViewSet(viewsets.GenericViewSet):
    permission_classes = (AllowAny,)
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(details=False, methods=['post'])
    def sign_up(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid()

        if self.get_queryset():
            return Response({'Message': "Email already exist"}, status=status.HTTP_400_BAD_REQUEST)
        if serializer.validated_data['password'] != serializer.validated_data['password_repeat']:
            return Response({'Message': "Passwords are not similar"}, status=status.HTTP_400_BAD_REQUEST)
        if serializer.validated_data['email'] is None or\
                serializer.validated_data['password'] is None or\
                serializer.validated_data['password_repeat'] is None:
            return Response({'Message': "Missing required args"}, status=status.HTTP_400_BAD_REQUEST)

        user = serializer.save()

        return Response(user, status=status.HTTP_201_CREATED)

    def filter_queryset(self, queryset: QuerySet) -> QuerySet:
        if self.action == 'sign_up':
            email = self.request.data.get('email')
            return super().filter_queryset(queryset).get(email=email)
