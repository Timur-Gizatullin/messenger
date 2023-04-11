from django.db import models

from core.models.mixins import CreatedAtUpdatedAtMixin
from core.utils.enums import AttachmentTypeEnum


class Attachment(CreatedAtUpdatedAtMixin):
    chat = models.ForeignKey("Chat", on_delete=models.CASCADE, related_name="attachments", verbose_name="Чат")
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="attachments", verbose_name="Пользователь")
    file = models.FileField(upload_to="attachments/", verbose_name="вложение")
    type = models.CharField(
        max_length=100,
        choices=AttachmentTypeEnum.get_choices(),
        default=AttachmentTypeEnum.FILE,
        verbose_name="Тип вложения",
    )
