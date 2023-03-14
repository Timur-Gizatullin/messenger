from django.db.models import QuerySet
from rest_framework import viewsets, status
from rest_framework.authentication import BasicAuthentication
from rest_framework.mixins import ListModelMixin
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.serializers.message import MessageSerializer
from core.models import Message


class MessageViewSet(ListModelMixin, viewsets.GenericViewSet):
    authentication_classes = (BasicAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    pagination_class = LimitOffsetPagination
