from enum import Enum


class BaseEnum(str, Enum):
    @classmethod
    def get_choices(cls) -> list[tuple[str, str]]:
        return [(key.name, key.value) for key in cls]


class Action(str, Enum):
    DELETE = "DELETE"
    CREATE = "CREATE"
    UPDATE = "UPDATE"


class ChatRoleEnum(BaseEnum):
    OWNER = "OWNER"
    ADMIN = "ADMIN"
    MEMBER = "MEMBER"
