import os
from typing import Literal, Optional
from pydantic import Field, model_validator
from ..operation import Operation


class Include(Operation):
    type: Literal["Include"] = Field(default="Include")
    file: Optional[str] = Field(default=None, description="File path to read")
    key: Optional[str] = Field(default=None, description="Dictionary key to read")
    head: Optional[int] = Field(default=0, description="Number of lines from the beginning to retain")
    tail: Optional[int] = Field(default=0, description="Number of lines from the end to retain")
    prefix: Optional[str] = Field(default=None, description="String to insert before data")
    suffix: Optional[str] = Field(default=None, description="String to insert after data")

    @model_validator(mode='after')
    def validate_file_key(self):
        if not self.file and not self.key:
            raise ValueError("Either 'file' or 'key' must be specified")
        if self.file and self.key:
            raise ValueError("'file' and 'key' are mutually exclusive")
        return self

    def _get_lines(self, data: str) -> list[str]:
        return data.splitlines(keepends=True)

    def phase_one(self, data: str, state: dict) -> str:
        lines = self._get_lines(data)
        print(lines, len(lines))
        count = len(lines)
        head = self.head or 0
        tail = self.tail or 0

        if head + tail > count:
            raise ValueError(f"head + tail must be less than the number of lines {count}")

        a = lines[:head]
        b = lines[-tail:] if tail > 0 else []
        return "".join(a + b)

    def phase_two(self, data: str, state: dict) -> str:
        # Resolve content x
        if self.file:
            if not (os.path.isfile(self.file) or os.path.islink(self.file)):
                raise ValueError(f"Invalid file path: {self.file}")
            with open(self.file, 'r', encoding='utf-8') as f:
                x = f.read()
        elif self.key:
            if self.key not in state:
                raise ValueError(f"Key '{self.key}' not found in state")
            x = state[self.key]
        else:
            # Should be caught by validator, but safe guard
            raise ValueError("No file or key specified")

        lines = self._get_lines(data)
        head = self.head or 0
        tail = self.tail or 0

        # Note: phase_two spec does not explicitly mandate the head+tail error check
        a = lines[:head]
        b = lines[-tail:] if tail > 0 else []

        prefix = self.prefix or ""
        suffix = self.suffix or ""

        return "".join(a) + prefix + x + suffix + "".join(b)