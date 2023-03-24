from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, status
from rest_framework.authentication import BasicAuthentication
from rest_framework.mixins import ListModelMixin
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from api.serializers.user import UserSerializer
from api.views.mixins import offset, limit
from core.models import User


class UserViewSet(ListModelMixin, viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return UserSerializer

    @swagger_auto_schema(manual_parameters=[limit, offset])
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        paginator = LimitOffsetPagination()
        page = paginator.paginate_queryset(queryset, request, view=self)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
