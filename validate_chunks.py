# validate_chunks.py
from typing import Optional, Any, Literal
from pydantic import BaseModel, ConfigDict

class Begin(BaseModel):
    model_config = ConfigDict(extra='forbid')

    type: Literal["Begin"]
    source: str
    shift: Optional[int] = None
    skip: Optional[int] = None
    add: Optional[int] = None

class End(BaseModel):
    model_config = ConfigDict(extra='forbid')

    type: Literal["End"]

def validate_chunks(x: list[Any]) -> None:
    for item in x:
        if isinstance(item, list):
            if len(item) != 3:
                raise ValueError("Invalid sub-list length")
            if not isinstance(item[0], dict):
                raise ValueError("Invalid item type")
            if not isinstance(item[1], str):
                raise ValueError("Invalid item type")
            if not isinstance(item[2], dict):
                raise ValueError("Invalid item type")

            for d in (item[0], item[2]):
                t = d.get("type")
                if t == "Begin":
                    Begin(**d)
                elif t == "End":
                    End(**d)
                else:
                    raise ValueError("Invalid parameter: type")