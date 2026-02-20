from typing import Literal
from ..transclude_base import TranscludeBase


class Uppercase(TranscludeBase):
    type: Literal["Uppercase"] = "Uppercase"

    def execute(self, data: str, state: dict) -> str:
        return data.upper()