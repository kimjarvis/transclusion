import os
from typing import Optional, Literal
from pydantic import Field, model_validator
from ..operation import Operation


class Include(Operation):
    type: Literal["Include"] = Field(default="Include")
    file: Optional[str] = Field(None, description="File path to read")
    key: Optional[str] = Field(None, description="Dictionary key to read")
    head: Optional[int] = Field(None, description="Number of lines from the beginning to retain")
    tail: Optional[int] = Field(None, description="Number of lines from the end to retain")

    @model_validator(mode='after')
    def validate_file_key_xor(self):
        if (self.file is None) == (self.key is None):
            raise ValueError("Exactly one of 'file' or 'key' must be specified")
        return self

    def _get_lines(self, data: str) -> list[str]:
        return data.splitlines(keepends=True)

    def _slice_data(self, data: str, head: int, tail: int) -> tuple[str, str]:
        lines = self._get_lines(data)
        print(lines)
        count = len(lines)
        if head + tail > count:
            raise ValueError(f"head ({head}) + tail ({tail}) exceeds number of lines ({count})")

        a = "".join(lines[:head])
        b = "".join(lines[-tail:]) if tail > 0 else ""
        return a, b

    def phase_one(self, data: str, state: dict) -> str:
        head = self.head or 0
        tail = self.tail or 0
        a, b = self._slice_data(data, head, tail)
        return a + b

    def phase_two(self, data: str, state: dict) -> str:
        head = self.head or 0
        tail = self.tail or 0

        if self.file:
            if not os.path.isfile(self.file):
                raise ValueError(f"File path or symbolic link expected: {self.file}")
            with open(self.file, 'r', encoding='utf-8') as f:
                x = f.read()
        else:
            if self.key not in state:
                raise ValueError(f"Key '{self.key}' not found in state")
            x = state[self.key]

        a, b = self._slice_data(data, head, tail)
        return a + x + b