from django.db import models
from rest_framework.exceptions import ValidationError

from core import constants
from core.models.mixins import CreatedAtUpdatedAtMixin


class MessageManager(models.Manager):
    @staticmethod
    def is_part_of_chat(chat_id: int, message: "Message"):
        if message.chat.pk != chat_id:
            raise ValidationError("Chosen message is not part of chat")


class Message(CreatedAtUpdatedAtMixin):
    author = models.ForeignKey(
        "User", on_delete=models.SET("DELETED"), related_name="messages", verbose_name="Отправитель"
    )
    chat = models.ForeignKey(
        "Chat", on_delete=models.CASCADE, related_name="messages", verbose_name="Чат, содержащий данное сообщение"
    )
    replied_to = models.ForeignKey(
        "Message",
        on_delete=models.SET_NULL,
        related_name="replied_messages",
        null=True,
        blank=True,
        verbose_name="Сообщение на которое ответили",
    )
    forwarded_by = models.ForeignKey(
        "User",
        on_delete=models.SET(constants.DELETED_USER),
        related_name="forwarded_messages",
        null=True,
        blank=True,
        verbose_name="Кем сообщение было переслано",
    )
    text = models.CharField(max_length=255, null=False, verbose_name="Текст сообщения")

    objects = MessageManager()
