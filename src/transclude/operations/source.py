from typing import Optional, Literal
from pydantic import Field, model_validator
from ..operation import Operation
from ..split import split

class Source(Operation):
    type: Literal["Source"] = Field(default="Source")
    file: Optional[str] = Field(default=None, description="File path to write")
    key: Optional[str] = Field(default=None, description="Dictionary key to write")
    head: Optional[int] = Field(default=None, description="Number of lines from the beginning to skip")
    tail: Optional[int] = Field(default=None, description="Number of lines from the end to skip")
    front: Optional[int] = Field(default=None, description="Number of characters from the beginning to skip")
    bask: Optional[int] = Field(default=None, description="Number of characters from the end to skip")

    @model_validator(mode='after')
    def check_file_key_xor(self):
        if bool(self.file) == bool(self.key):
            raise ValueError("Exactly one of 'file' or 'key' must be specified")
        return self

    def phase_one(self, data: str, state: dict) -> str:
        _, b, _ = split(
            data,
            self.head or 0,
            self.front or 0,
            self.bask or 0,
            self.tail or 0
        )
        if self.file:
            with open(self.file, 'w') as f:
                f.write(b)
        elif self.key:
            state[self.key] = b
        return data

    def phase_two(self, data: str, state: dict) -> str:
        return data