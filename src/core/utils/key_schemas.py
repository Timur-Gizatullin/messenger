from typing import Any


class BaseKeySchema:
    prefix: str
    delimiter = "_"

    def __init__(self, prefix: str):
        self.prefix = prefix

    def get_key(self, postfix: Any) -> str:
        return f"{self.prefix}{self.delimiter}{postfix}"
