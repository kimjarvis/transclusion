from typing import Optional, Literal
from pydantic import Field, model_validator
from ..operation import Operation


class Source(Operation):
    type: Literal["Source"] = Field(default="Source")
    file: Optional[str] = Field(default=None, description="File path to write")
    key: Optional[str] = Field(default=None, description="Dictionary key to write")
    head: Optional[int] = Field(default=None, description="Number of lines from the beginning to retain")
    tail: Optional[int] = Field(default=None, description="Number of lines from the end to retain")

    @model_validator(mode='after')
    def validate_xor(self):
        if not self.file and not self.key:
            raise ValueError("Either 'file' or 'key' must be specified")
        if self.file and self.key:
            raise ValueError("'file' and 'key' are mutually exclusive")
        return self

    def phase_one(self, data: str, state: dict) -> str:
        lines = data.splitlines()

        if self.head:
            lines = lines[self.head:]
        if self.tail:
            lines = lines[:-self.tail]

        result = "\n".join(lines)

        if self.file:
            with open(self.file, 'w', encoding='utf-8') as f:
                f.write(result)
        elif self.key:
            state[self.key] = result

        return result

    def phase_two(self, data: str, state: dict) -> str:
        return data