from abc import ABC, abstractmethod
from typing import Optional
from pydantic import BaseModel, ConfigDict

class Base(BaseModel, ABC):
    @abstractmethod
    def execute(self, data: str) -> str:
        pass

class Uppercase(Base):
    model_config = ConfigDict(extra='forbid')
    type: str

    def execute(self, data: str) -> str:
        return data.upper()

class Begin(Base):
    model_config = ConfigDict(extra='forbid')
    type: str
    source: str
    shift: Optional[int] = None
    skip: Optional[int] = None
    add: Optional[int] = None

    def execute(self, data: str) -> str:
        return data

class End(Base):
    model_config = ConfigDict(extra='forbid')
    type: str

    def execute(self, data: str) -> str:
        return data

