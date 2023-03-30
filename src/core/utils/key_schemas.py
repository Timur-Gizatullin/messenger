class BaseKeySchema:
    delimiter = "_"

    def __init__(self, prefix: str):
        self.prefix = prefix

    def get_key(self, postfix: str | None = None, path: str | None = None) -> str:
        if path:
            return f"{self.prefix}{self.delimiter}{path.split('/')[-1]}"

        return f"{self.prefix}{self.delimiter}{postfix}"
