from typing import Literal
from ..directive import Directive

class Uppercase(Directive):
    syncspec: Literal["Uppercase"] = "Uppercase"

    def phase_one(self, data: str, state: dict) -> str:
        return data

    def phase_two(self, data: str, state: dict) -> str:
        return data.upper()