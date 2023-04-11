from enum import Enum


class Action(str, Enum):
    DELETE = "DELETE"
    CREATE = "CREATE"
    UPDATE = "UPDATE"


class ChatRoleEnum(str, Enum):
    OWNER = "OWNER"
    ADMIN = "ADMIN"
    MEMBER = "MEMBER"

    @classmethod
    def get_choices(cls) -> list[tuple[str, str]]:
        return [(key.value, key.name) for key in cls]
