from typing import Optional, Literal
from pydantic import Field, model_validator
from ..operation import Operation


class Source(Operation):
    type: Literal["Source"] = Field(default="Source")
    file: Optional[str] = Field(default=None, description="File path to write")
    key: Optional[str] = Field(default=None, description="Dictionary key to write")
    head: Optional[int] = Field(default=None, description="Number of lines from the beginning to skip")
    tail: Optional[int] = Field(default=None, description="Number of lines from the end to skip")
    strip: Optional[str] = Field(default=None, description="Strip characters from the beginning and end")
    lstrip: Optional[str] = Field(default=None, description="Strip characters from the beginning")
    rstrip: Optional[str] = Field(default=None, description="Strip characters from the end")

    @model_validator(mode='after')
    def validate_file_key_exclusivity(self):
        if not self.file and not self.key:
            raise ValueError("Either 'file' or 'key' must be specified")
        if self.file and self.key:
            raise ValueError("'file' and 'key' are mutually exclusive")
        return self

    def phase_one(self, data: str, state: dict) -> str:
        original_data = data
        lines = data.splitlines(keepends=True)

        # Head
        if self.head:
            lines = lines[self.head:]

        # Tail
        if self.tail:
            lines = lines[:-self.tail] if len(lines) > self.tail else []

        data = "".join(lines)

        # Strip
        if self.strip is not None:
            data = data.strip() if self.strip == "" else data.strip(self.strip)
        if self.lstrip is not None:
            data = data.lstrip() if self.lstrip == "" else data.lstrip(self.lstrip)
        if self.rstrip is not None:
            data = data.rstrip() if self.rstrip == "" else data.rstrip(self.rstrip)

        # Write
        if self.file:
            with open(self.file, 'w') as f:
                f.write(data)
        elif self.key:
            state[self.key] = data

        return original_data

    def phase_two(self, data: str, state: dict) -> str:
        return data