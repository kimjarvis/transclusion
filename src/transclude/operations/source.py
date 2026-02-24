from typing import Literal, Optional
from pydantic import Field, model_validator
from ..operation import Operation
from ..split import split

class Source(Operation):
    type: Literal["Source"] = Field(default="Source")
    file: Optional[str] = Field(default=None, description="File path to write")
    key: Optional[str] = Field(default=None, description="Dictionary key to write")
    head: int = Field(default=1, description="Number of lines from the head to skip")
    tail: int = Field(default=1, description="Number of lines from the tail to skip")

    @model_validator(mode='after')
    def validate_xor(self):
        if bool(self.file) == bool(self.key):
            raise ValueError("Exactly one of 'file' or 'key' must be specified")
        return self

    def phase_one(self, data: str, state: dict) -> str:
        result = split(data, self.head, self.tail)
        if self.file:
            with open(self.file, 'w') as f:
                f.write(result.middle)
        if self.key:
            state[self.key] = result.middle
        return data

    def phase_two(self, data: str, state: dict) -> str:
        return data