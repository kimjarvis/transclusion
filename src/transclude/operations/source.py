from typing import Optional, Literal, Dict, Any
from pathlib import Path
from pydantic import Field, model_validator

from ..operation import Operation

class Source(Operation):
    # init=False removed to allow explicit type="Source" instantiation required by tests
    type: Literal["Source"] = Field(default="Source")
    file: Optional[str] = Field(default=None, description="File path to write")
    key: Optional[str] = Field(default=None, description="Dictionary key to write")
    head: Optional[int] = Field(default=None, description="Number of lines from the beginning to skip")
    tail: Optional[int] = Field(default=None, description="Number of lines from the end to skip")
    strip: Optional[str] = Field(default=None, description="Strip characters from the beginning and end")
    lstrip: Optional[str] = Field(default=None, description="Strip characters from the beginning")
    rstrip: Optional[str] = Field(default=None, description="Strip characters from the end")

    @model_validator(mode='after')
    def validate_xor(self) -> 'Source':
        if (self.file is None) == (self.key is None):
            raise ValueError("Exactly one of 'file' or 'key' must be specified")
        return self

    def phase_one(self, data: str, state: dict) -> str:
        lines = data.splitlines(keepends=True)

        if self.head:
            lines = lines[self.head:]
        if self.tail:
            lines = lines[:-self.tail] if self.tail < len(lines) else []

        processed = "".join(lines)

        if self.strip is not None:
            processed = processed.strip() if self.strip == "" else processed.strip(self.strip)
        if self.lstrip is not None:
            processed = processed.lstrip() if self.lstrip == "" else processed.lstrip(self.lstrip)
        if self.rstrip is not None:
            processed = processed.rstrip() if self.rstrip == "" else processed.rstrip(self.rstrip)

        if self.file:
            Path(self.file).write_text(processed, encoding='utf-8')
        elif self.key:
            state[self.key] = processed

        return data

    def phase_two(self, data: str, state: dict) -> str:
        return data