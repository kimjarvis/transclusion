from typing import Optional, Literal
from pathlib import Path
from pydantic import Field

from ..operation import Operation


class Include(Operation):
    type: Literal["Include"] = Field(default="Include")
    source: str = Field(..., description="File path to include")
    head: Optional[int] = Field(default=0, description="Number of lines from the beginning to retain")
    tail: Optional[int] = Field(default=0, description="Number of lines from the end to retain")

    def execute(self, data: str, state: dict) -> str:
        head = self.head or 0
        tail = self.tail or 0

        path = Path(self.source)
        if not (path.is_file() or path.is_symlink()):
            raise ValueError(f"Source '{self.source}' is not a valid file or symbolic link")

        x = path.read_text(encoding="utf-8")
        lines = data.splitlines(keepends=True)
        print(lines)

        if head + tail > len(lines) + 1:
            raise ValueError(f"head ({head}) + tail ({tail}) exceeds number of lines ({len(lines)})")

        a = lines[:head]
        b = lines[-tail:] if tail > 0 else []

        return "".join(a) + x + "".join(b)