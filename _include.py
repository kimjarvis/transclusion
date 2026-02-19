from pathlib import Path
from pydantic import Field
from filters import Base  # Assumed import based on context

class Include(Base):
    type: str = Field(..., description="Include type")
    source: str = Field(..., alias="file", description="File path to include")

    def execute(self, data: str, state: dict) -> str:
        path = Path(self.source)
        if not (path.is_file() or path.is_symlink()):
            raise FileNotFoundError(f"Source must be a file or symlink: {self.source}")
        return path.read_text(encoding="utf-8")