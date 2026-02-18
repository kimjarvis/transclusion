from abc import ABC, abstractmethod
from typing import Optional
from pydantic import BaseModel, ConfigDict

class Base(BaseModel, ABC):
    model_config = ConfigDict(extra='forbid')

    @abstractmethod
    def execute(self, data: str) -> str:
        pass

class Uppercase(Base):
    type: str

    def execute(self, data: str) -> str:
        return data.upper()

class Begin(Base):
    type: str
    source: str
    shift: Optional[int] = None
    skip: Optional[int] = None
    add: Optional[int] = None

    def execute(self, data: str) -> str:
        return data

class End(Base):
    type: str

    def execute(self, data: str) -> str:
        return data

