from django.db.models import QuerySet
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.mixins import ListModelMixin
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from api.serializers.user import UserSerializer
from api.utils import limit, offset, default_limit, email

from core.models import User


class UserViewSet(ListModelMixin, viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return UserSerializer

    def filter_queryset(self, queryset: QuerySet) -> QuerySet:
        if self.action == "list":
            return super().filter_queryset(queryset).filter(email__contains=self.request.query_params["email"])

        return super().filter_queryset(queryset)

    @swagger_auto_schema(manual_parameters=[limit, offset, email])
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        if request.query_params.get("email", None):
            queryset = self.filter_queryset(queryset)

        paginator = LimitOffsetPagination()
        page = paginator.paginate_queryset(queryset, request, view=self)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
