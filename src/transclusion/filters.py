from abc import ABC, abstractmethod
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field
from pathlib import Path

class Base(BaseModel, ABC):
    model_config = ConfigDict(extra='forbid')

    @abstractmethod
    def execute(self, data: str, state: dict) -> str:
        pass

class Uppercase(Base):
    type: str

    def execute(self, data: str, state: dict) -> str:
        return data.upper()

class Begin(Base):
    type: str
    source: str
    shift: Optional[int] = None
    skip: Optional[int] = None
    add: Optional[int] = None

    def execute(self, data: str, state: dict) -> str:
        return data

class End(Base):
    type: str

    def execute(self, data: str, state: dict) -> str:
        return data

class Include(Base):
    type: str = Field(..., description="Include type")
    source: str = Field(..., description="File path to include")

    def execute(self, data: str, state: dict) -> str:
        path = Path(self.source)
        if not (path.is_file() or path.is_symlink()):
            raise FileNotFoundError(f"Source must be a file or symlink: {self.source}")
        return path.read_text(encoding="utf-8")