from abc import ABC, abstractmethod
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field

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
    source: str = Field(..., alias="file", description="File path to include")

    def execute(self, data: str, state: dict) -> str:
        return x
