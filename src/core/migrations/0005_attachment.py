# Generated by Django 4.1.7 on 2023-04-05 14:32

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0004_user_is_deleted_alter_chat_created_at_and_more"),
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
                    "chat",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="attachments",
                        to="core.chat",
                        verbose_name="Чат",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="attachments",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Пользователь",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]