from typing import TypeVar

from django.db import models
from rest_framework.exceptions import ValidationError

from core.models.mixins import CreatedAtUpdatedAtMixin

Message = TypeVar("Message")
Attachment = TypeVar("Attachment")


class ChatManager(models.Manager):
    @staticmethod
    def validate_before_create_message(user_id: int, chat_id: int) -> None:
        queryset = Chat.objects.filter(pk=chat_id)

        if not queryset.filter(users__id=user_id):
            raise ValidationError("User is not a member of the chosen chats")
        if queryset.filter(is_dialog=True).filter(users__is_deleted=True):
            raise ValidationError("one of users is deleted, dialog is not allowed")

    @staticmethod
    def is_object_part_of_chat(chat_id: int, chat_object: Message | Attachment | None):
        if chat_object and chat_object.chat.pk != chat_id:  # type: ignore
            raise ValidationError("Chosen object is not part of chat")


class Chat(CreatedAtUpdatedAtMixin):
    users = models.ManyToManyField("User", related_name="chats", verbose_name="Участники чата")
    is_dialog = models.BooleanField(default=True, verbose_name="Флаг, является ли чат диалогом")
    objects = ChatManager()
