from dataclasses import dataclass

from core.utils.enums import ActionEnum, WSMessageTypeEnum


@dataclass
class WSContent:
    type: ActionEnum
    data: dict


@dataclass
class WSMessage:
    type: WSMessageTypeEnum
    content: WSContent
