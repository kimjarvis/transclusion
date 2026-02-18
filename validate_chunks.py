from typing import Any
from pydantic import BaseModel


class ChunkValidator:
    def __init__(self):
        self._registry: dict[str, type[BaseModel]] = {}

    def register(self, filer: str, cls: Any):
        self._registry[filer] = cls

    def validate_chunks(self, x: list[Any]) -> list[Any]:
        result = []
        for item in x:
            if isinstance(item, str):
                result.append(item)
            elif isinstance(item, list):
                result.append(self._validate_sub_list(item))
            else:
                raise ValueError("Invalid type")
        return result

    def _validate_sub_list(self, sub: list[Any]) -> list[Any]:
        if len(sub) != 5:
            raise ValueError("Invalid sub-list length")

        types = [str, dict, str, str, dict]
        for i, t in enumerate(types):
            if not isinstance(sub[i], t):
                raise ValueError(f"Invalid sub-list type at position {i}")

        objs = []
        for idx in [1, 4]:
            d = sub[idx]
            if "type" not in d:
                raise ValueError("Missing type key")
            type_name = d["type"]
            if type_name not in self._registry:
                raise ValueError(f"Unknown type: {type_name}")
            objs.append(self._registry[type_name](**d))

        return [sub[0], sub[1], objs[0], sub[2], sub[3], sub[4], objs[1]]