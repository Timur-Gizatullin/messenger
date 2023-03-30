from enum import Enum


class Action(str, Enum):
    DELETE = "DELETE"
    CREATE = "CREATE"
    UPDATE = "UPDATE"
