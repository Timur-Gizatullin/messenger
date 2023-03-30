from dataclasses import dataclass

from core.utils.enums import Action


@dataclass
class WSContent:
    type: Action
    data: str


@dataclass
class WSMessage:
    type: str
    content: WSContent
