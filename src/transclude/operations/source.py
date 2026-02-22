from typing import Optional, Literal, Dict, Any
from pathlib import Path
from pydantic import Field, model_validator

from ..operation import Operation


class Source(Operation):
    type: Literal["Source"] = Field(default="Source")
    file: Optional[str] = Field(default=None, description="File path to write")
    key: Optional[str] = Field(default=None, description="Dictionary key to write")
    head: Optional[int] = Field(default=None, description="Number of lines from the beginning to retain")
    tail: Optional[int] = Field(default=None, description="Number of lines from the end to retain")

    @model_validator(mode='after')
    def validate_xor(self) -> 'Source':
        if (self.file is None) == (self.key is None):
            raise ValueError("Exactly one of 'file' or 'key' must be specified")
        return self

    def phase_one(self, data: str, state: Dict[str, Any]) -> str:
        lines = data.splitlines(keepends=True)

        if self.head:
            lines = lines[self.head:]
        if self.tail:
            lines = lines[:-self.tail] if self.tail < len(lines) else []

        trimmed = "".join(lines)

        if self.file:
            Path(self.file).write_text(trimmed, encoding='utf-8')
        elif self.key:
            state[self.key] = trimmed

        return data

    def phase_two(self, data: str, state: Dict[str, Any]) -> str:
        return data