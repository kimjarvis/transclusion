from typing import Optional
from pydantic import Field
from pathlib import Path

from ..transclude_base import TranscludeBase

class Include(TranscludeBase):
    type: str = Field(..., description="Include type")
    source: str = Field(..., description="File path to include")
    skip: Optional[int] = None
    add: Optional[int] = None

    def execute(self, data: str, state: dict) -> str:
        path = Path(self.source)
        if not (path.is_file() or path.is_symlink()):
            raise FileNotFoundError(f"Source must be a file or symlink: {self.source}")
        return path.read_text(encoding="utf-8")