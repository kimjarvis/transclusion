from typing import Literal
from ..operation import Operation

class Uppercase(Operation):
    type: Literal["Uppercase"] = "Uppercase"

    def phase_one(self, data: str, state: dict) -> str:
        return data

    def phase_two(self, data: str, state: dict) -> str:
        return data.upper()