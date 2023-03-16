# Generated by Django 4.1.7 on 2023-03-10 11:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Chat",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Время создания чата"
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(
                        auto_now=True,
                        null=True,
                        verbose_name="Время последнего изменения чата",
                    ),
                ),
                (
                    "is_dialog",
                    models.BooleanField(
                        default=True, verbose_name="Флаг, является ли чат диалогом"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="User",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "email",
                    models.CharField(
                        max_length=255, unique=True, verbose_name="Почта пользователя"
                    ),
                ),
                (
                    "password",
                    models.CharField(
                        max_length=255, verbose_name="Пароль пользователя"
                    ),
                ),
                (
                    "registered_at",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Время регистрации"
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(
                        auto_now=True,
                        null=True,
                        verbose_name="Время последнего изменения профиля",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        max_length=255, null=True, verbose_name="Имя пользователя"
                    ),
                ),
                (
                    "surname",
                    models.CharField(
                        max_length=255, null=True, verbose_name="Фамилия пользователя"
                    ),
                ),
                (
                    "profile_picture",
                    models.ImageField(upload_to="", verbose_name="Фотография профиля"),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Message",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "text",
                    models.CharField(
                        max_length=255, null=True, verbose_name="Текст сообщения"
                    ),
                ),
                (
                    "picture",
                    models.ImageField(
                        null=True, upload_to="", verbose_name="Картинка сообщения"
                    ),
                ),
                (
                    "sent_at",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Время отправки сообщения"
                    ),
                ),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="author",
                        to="core.user",
                        verbose_name="Отправитель",
                    ),
                ),
                (
                    "chat",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="chat",
                        to="core.chat",
                        verbose_name="Чат, содержащий данное сообщение",
                    ),
                ),
                (
                    "forward_by",
                    models.OneToOneField(
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="forward_by",
                        to="core.user",
                        verbose_name="Кем сообщение было переслано",
                    ),
                ),
                (
                    "reply_to",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="replied_to",
                        to="core.message",
                        verbose_name="Сообщение на которое ответили",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="chat",
            name="last_message",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="last_message",
                to="core.message",
                verbose_name="Последнее сообщение чата",
            ),
        ),
        migrations.AddField(
            model_name="chat",
            name="users",
            field=models.ManyToManyField(
                related_name="users", to="core.user", verbose_name="Участники чата"
            ),
        ),
    ]
