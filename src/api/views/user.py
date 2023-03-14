from django.db.models import QuerySet
from rest_framework import viewsets
from rest_framework.authentication import BasicAuthentication
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated

from api.serializers.user import UserSerializer
from core.models import User


class UserViewSet(RetrieveModelMixin, viewsets.GenericViewSet):
    authentication_classes = (BasicAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def filter_queryset(self, queryset: QuerySet) -> QuerySet:
        if self.action == 'retrieve':
            return super().filter_queryset(queryset).filter(email__contains=self.request.data['user_to_find'])
