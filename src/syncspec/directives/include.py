from typing import Literal, Optional
from pathlib import Path
from pydantic import Field, model_validator

from ..directive import Directive
from ..split import split


class Include(Directive):
    type: Literal["Include"] = Field(default="Include")
    file: Optional[str] = Field(default=None, description="File path to read")
    key: Optional[str] = Field(default=None, description="Dictionary key to read")
    head: int = Field(default=1, description="Number of lines from the head to skip")
    tail: int = Field(default=1, description="Number of lines from the tail to skip")

    @model_validator(mode='after')
    def check_file_key_exclusive(self):
        if (self.file is None) == (self.key is None):
            raise ValueError("Exactly one of 'file' or 'key' must be specified")
        return self

    def phase_one(self, data: str, state: dict) -> str:
        result = split(data, self.head, self.tail)
        return result.top + result.bottom

    def phase_two(self, data: str, state: dict) -> str:
        x = ""
        if self.file:
            path = Path(self.file)
            if not path.is_file():
                raise FileNotFoundError(f"File not found: {self.file}")
            x = path.read_text(encoding='utf-8')
        elif self.key:
            if self.key not in state:
                raise KeyError(f"Key not found in state: {self.key}")
            x = state[self.key]

        result = split(data, self.head, self.tail)
        return result.top + x + result.bottom