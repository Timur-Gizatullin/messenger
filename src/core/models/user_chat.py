from django.db import models

from core.utils.enums import ChatRoleEnum


class UserChatManager(models.Manager):
    @staticmethod
    def is_user_has_permission_to_update_role(user_role: ChatRoleEnum) -> bool:
        return user_role == ChatRoleEnum.OWNER or user_role == ChatRoleEnum.ADMIN

    @staticmethod
    def is_user_under_update_owner(user_role: ChatRoleEnum) -> bool:
        return user_role == ChatRoleEnum.OWNER


class UserChat(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, verbose_name="Пользователь")
    chat = models.ForeignKey("Chat", on_delete=models.CASCADE, verbose_name="Чат")
    role = models.CharField(
        max_length=100,
        verbose_name="Роль пользователя в чате",
        choices=ChatRoleEnum.get_choices(),
        default=ChatRoleEnum.MEMBER,
    )

    objects = UserChatManager()
