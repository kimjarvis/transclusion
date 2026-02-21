from typing import Literal
from ..operation import Operation

class Uppercase(Operation):
    type: Literal["Uppercase"] = "Uppercase"

    def execute(self, data: str, state: dict) -> str:
        return data.upper()