# Generated by Django 4.1.7 on 2023-04-17 11:18

import core.utils.enums
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0006_remove_message_picture"),
    ]

    operations = [
        migrations.CreateModel(
            name="Attachment",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="Время создания")),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, null=True, verbose_name="Время последнего изменения"),
                ),
                ("file", models.FileField(upload_to="attachments/", verbose_name="вложение")),
                (
                    "type",
                    models.CharField(
                        choices=[("PICTURE", "PICTURE"), ("FILE", "FILE")],
                        default=core.utils.enums.AttachmentTypeEnum["FILE"],
                        max_length=100,
                        verbose_name="Тип вложения",
                    ),
                ),
                (
                    "chat",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="attachments",
                        to="core.chat",
                        verbose_name="Чат",
                    ),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        on_delete=models.SET("DELETED_USER"),
                        related_name="attachments",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Отправитель",
                    ),
                ),
                (
                    "forwarded_by",
                    models.ForeignKey(
                        null=True,
                        on_delete=models.SET("DELETED_USER"),
                        related_name="forwarded_attachments",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Кем переслано вложение",
                    ),
                ),
                (
                    "reply_to_attachment",
                    models.ForeignKey(
                        null=True,
                        on_delete=models.SET("DELETED_ATTACHMENT"),
                        related_name="replied_attachments_by_attachment",
                        to="core.attachment",
                        verbose_name="Вложение, на которое ответили",
                    ),
                ),
                (
                    "reply_to_message",
                    models.ForeignKey(
                        null=True,
                        on_delete=models.SET("DELETED_MESSAGE"),
                        related_name="replied_messages_by_attachment",
                        to="core.message",
                        verbose_name="Сообщение, на которое ответили",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
