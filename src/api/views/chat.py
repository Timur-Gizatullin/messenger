from django.db.models import QuerySet
from rest_framework import viewsets
from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.mixins import CreateModelMixin
from rest_framework.response import Response

from api.serializers.chat import ChatSerializer, ChatCreateSerializer
from core.models import Chat


class ChatViewSet(CreateModelMixin, ListModelMixin, viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Chat.objects.all()

    def create(self, request, *args, **kwargs):
        if not [user['pk'] for user in request.data['users']].__contains__(request.user.id):
            return Response({"Message": "Impossible create chat without current user as member"})

        return super().create(request, *args, **kwargs)

    def filter_queryset(self, queryset: QuerySet) -> QuerySet:
        if self.action == "list":
            return super().filter_queryset(queryset).filter(users=self.request.user)
        else:
            return super().filter_queryset(queryset)

    def get_serializer_class(self):
        if self.action == 'list':
            return ChatSerializer
        elif self.action == 'create':
            return ChatCreateSerializer
