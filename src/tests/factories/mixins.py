from typing import Any

from factory import Faker
from factory.builder import BuildStep


class UniqueStringMixin(Faker):
    def evaluate(self, instance: Any, step: BuildStep, extra: Any) -> str:
        value = super().evaluate(instance, step, extra)
        return f"{step.sequence} {value}"
