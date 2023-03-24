from django.db.models import QuerySet
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from api.serializers.user import UserSerializer
from api.views.mixins import email
from core.models import User


class UserViewSet(ListModelMixin, viewsets.GenericViewSet):
    permission_classes = (AllowAny,)
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def filter_queryset(self, queryset: QuerySet) -> QuerySet:
        if self.action == "find_user":
            return super().filter_queryset(queryset).filter(email__contains=self.request.query_params["email"])

        return super().filter_queryset(queryset)

    def get_queryset(self):
        return User.objects.all()

    @swagger_auto_schema(manual_parameters=[email])
    @action(detail=False, methods=["GET"], url_path="find")
    def find_user(self, request, *args, **kwargs):
        if not request.query_params.get("email", None):
            serializer = self.get_serializer(self.queryset, many=True)
            return Response(serializer.data)

        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data)
