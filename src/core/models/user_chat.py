from django.db import models

from core.utils.enums import ChatRoleEnum


class UserChat(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, verbose_name="Пользователь")
    chat = models.ForeignKey("Chat", on_delete=models.CASCADE, verbose_name="Чат")
    role = models.CharField(
        max_length=100,
        verbose_name="Роль пользователя в чате",
        choices=ChatRoleEnum.get_choices(),
        default=ChatRoleEnum.MEMBER,
    )

    def is_chat_owner(self) -> bool:
        return self.role == ChatRoleEnum.OWNER

    def can_update_roles(self) -> bool:
        return self.role in (ChatRoleEnum.OWNER, ChatRoleEnum.ADMIN)

    def can_add_or_delete_user_from_chat(self) -> bool:
        return self.role in (ChatRoleEnum.OWNER, ChatRoleEnum.ADMIN)
