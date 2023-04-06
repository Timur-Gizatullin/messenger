from django.db import models
from rest_framework.exceptions import ValidationError

from core.models.mixins import CreatedAtUpdatedAtMixin


class ChatManager(models.Manager):
    def validate_before_create_message(self, user_id: int, chat_id: int) -> None:
        queryset = Chat.objects.filter(pk=chat_id)

        if not queryset.filter(users__id=user_id):
            raise ValidationError("User is not a member of the current chat")
        if queryset.filter(is_dialog=True).filter(users__is_deleted=True):
            raise ValidationError("one of users is deleted, dialog is not allowed")


class Chat(CreatedAtUpdatedAtMixin):
    users = models.ManyToManyField("User", related_name="chats", verbose_name="Участники чата")
    is_dialog = models.BooleanField(default=True, verbose_name="Флаг, является ли чат диалогом")
    objects = ChatManager()
