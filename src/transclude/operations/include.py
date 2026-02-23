from pathlib import Path
from typing import Literal, Optional

from pydantic import Field, model_validator

from ..operation import Operation
from ..split import split


class Include(Operation):
    type: Literal["Include"] = Field(default="Include")
    file: Optional[str] = Field(default=None, description="File path to read")
    key: Optional[str] = Field(default=None, description="Dictionary key to read")
    head: Optional[int] = Field(default=None, description="Number of lines from the beginning to retain")
    tail: Optional[int] = Field(default=None, description="Number of lines from the end to retain")
    front: Optional[int] = Field(default=None, description="Number of characters from the beginning to retain")
    back: Optional[int] = Field(default=None, description="Number of characters from the end to retain")

    @model_validator(mode='after')
    def validate_file_xor_key(self):
        if (self.file is None) == (self.key is None):
            raise ValueError("Exactly one of 'file' or 'key' must be specified")
        return self

    def phase_one(self, data: str, state: dict) -> str:
        res = split(
            data,
            self.head or 0,
            self.front or 0,
            self.back or 0,
            self.tail or 0
        )
        return res.first + res.last

    def phase_two(self, data: str, state: dict) -> str:
        res = split(
            data,
            self.head or 0,
            self.front or 0,
            self.back or 0,
            self.tail or 0
        )

        if self.file:
            path = Path(self.file)
            if not path.exists():
                raise FileNotFoundError(f"File not found: {self.file}")
            x = path.read_text(encoding='utf-8')
        else:
            if self.key not in state:
                raise KeyError(f"Key not found in state: {self.key}")
            x = state[self.key]

        return res.first + x + res.last