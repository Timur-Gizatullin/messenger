from enum import Enum


class AttachmentTypeEnum(str, Enum):
    PICTURE = "PICTURE"
    FILE = "FILE"

    @classmethod
    def get_choices(cls) -> list[tuple[str, str]]:
        return [(key.value, key.name) for key in cls]
