from dataclasses import dataclass

from core.utils.enums import ActionEnum, WSType


@dataclass
class WSContent:
    type: ActionEnum
    data: dict


@dataclass
class WSMessage:
    type: WSType
    content: WSContent
