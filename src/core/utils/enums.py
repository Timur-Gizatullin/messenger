from enum import Enum


class Action(str, Enum):
    DELETE = 1,
    CREATE = 2,
    UPDATE = 3
