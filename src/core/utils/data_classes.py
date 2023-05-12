from dataclasses import dataclass

from core.utils.enums import ActionEnum


@dataclass
class WSContent:
    type: ActionEnum
    data: dict


@dataclass
class WSMessage:
    type: str
    content: WSContent
