from enum import Enum


class BaseEnum(str, Enum):
    @classmethod
    def get_choices(cls) -> list[tuple[str, str]]:
        return [(key.name, key.value) for key in cls]


class ActionEnum(str, Enum):
    DELETE = "DELETE"
    CREATE = "CREATE"
    UPDATE = "UPDATE"


class AttachmentTypeEnum(BaseEnum):
    PICTURE = "PICTURE"
    FILE = "FILE"


attachments_type_map = {
    "image/png": AttachmentTypeEnum.PICTURE,
}


class ChatRoleEnum(BaseEnum):
    OWNER = "OWNER"
    ADMIN = "ADMIN"
    MEMBER = "MEMBER"
