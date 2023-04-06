class BaseKeySchema:
    delimiter = "_"

    def __init__(self, prefix: str):
        self.prefix = prefix

    def get_key(self, postfix: list[str]) -> str:
        handled_postfix = f"{self.delimiter}".join(postfix)
        return f"{self.prefix}{self.delimiter}{handled_postfix}"
