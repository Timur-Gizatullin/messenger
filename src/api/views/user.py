from django.db.models import QuerySet
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.parsers import MultiPartParser, JSONParser
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from api.serializers.user import UserSerializer, UploadProfilePicSerializer
from api.utils import limit, offset, email

from core.models import User


class UserViewSet(ListModelMixin, viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()

    def get_parsers(self):
        if self.action_map.get("post", None) and self.action_map["post"] == "upload_profile_picture":
            return [
                MultiPartParser(),
            ]

        return [
            JSONParser(),
        ]

    def get_serializer_class(self):
        if self.action == "list":
            return UserSerializer
        if self.action == "upload_profile_picture":
            return UploadProfilePicSerializer

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

    @action(detail=False, methods=["POST"])
    def upload_profile_picture(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)
