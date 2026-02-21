from typing import Literal, Optional
from pathlib import Path
from pydantic import Field
from ..operation import Operation


class Include(Operation):
    type: Literal["Include"] = Field(default="Include")
    source: str = Field(..., description="File path to include")
    head: Optional[int] = Field(default=None, description="Number of lines from the beginning to retain")
    tail: Optional[int] = Field(default=None, description="Number of lines from the end to retain")

    def _slice_data(self, data: str) -> tuple[str, str]:
        h = self.head or 0
        t = self.tail or 0
        lines = data.splitlines(keepends=True)

        if h + t > len(lines):
            raise ValueError("head + tail cannot exceed number of lines")

        a = "".join(lines[:h])
        b = "".join(lines[-t:]) if t > 0 else ""
        return a, b

    def phase_one(self, data: str, state: dict) -> str:
        a, b = self._slice_data(data)
        return a + b

    def phase_two(self, data: str, state: dict) -> str:
        path = Path(self.source)
        if not (path.is_file() or path.is_symlink()):
            raise ValueError(f"Source {self.source} is not a file or symbolic link")

        x = path.read_text(encoding="utf-8")
        a, b = self._slice_data(data)
        return a + x + b