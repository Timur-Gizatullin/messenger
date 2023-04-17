from django.db import models
from rest_framework.exceptions import ValidationError

from core import constants
from core.models.mixins import CreatedAtUpdatedAtMixin
from core.utils.enums import AttachmentTypeEnum


class AttachmentManager(models.Manager):
    @staticmethod
    def is_object_part_of_chat(chat_id: int, attachment: type("Attachment") | None):
        if attachment and attachment.chat.pk != chat_id:  # type: ignore
            raise ValidationError("Chosen attachment is not part of chat")


class Attachment(CreatedAtUpdatedAtMixin):
    created_by = models.ForeignKey(
        "User",
        on_delete=models.SET(constants.DELETED_USER),
        related_name="attachments",
        verbose_name="Отправитель",
    )
    chat = models.ForeignKey(
        "Chat",
        on_delete=models.CASCADE,
        related_name="attachments",
        verbose_name="Чат",
    )
    reply_to_message = models.ForeignKey(
        "Message",
        on_delete=models.SET(constants.DELETED_MESSAGE),
        related_name="replied_messages_by_attachment",
        verbose_name="Сообщение, на которое ответили",
        null=True,
    )
    reply_to_attachment = models.ForeignKey(
        "Attachment",
        on_delete=models.SET(constants.DELETED_ATTACHMENT),
        related_name="replied_attachments_by_attachment",
        verbose_name="Вложение, на которое ответили",
        null=True,
    )
    forwarded_by = models.ForeignKey(
        "User",
        on_delete=models.SET(constants.DELETED_USER),
        related_name="forwarded_attachments",
        verbose_name="Кем переслано вложение",
        null=True,
    )
    file = models.FileField(upload_to="attachments/", verbose_name="вложение")
    type = models.CharField(
        max_length=100,
        choices=AttachmentTypeEnum.get_choices(),
        default=AttachmentTypeEnum.FILE,
        verbose_name="Тип вложения",
    )

    objects = AttachmentManager()
