from typing import Any
from pydantic import BaseModel

class Registry:
    def __init__(self):
        self._registry = {}

    def register(self, filer: str, cls: Any):
        self._registry[filer] = cls

    def dictionaries_to_directives(self, x: list[Any]) -> list[Any]:
        result = []
        for item in x:
            if isinstance(item, str):
                result.append(item)
            elif isinstance(item, list):
                result.append(self._validate_sublist(item))
            else:
                raise ValueError("Invalid type")
        return result

    def _validate_sublist(self, sub: list) -> list:
        if len(sub) != 5:
            raise ValueError("Invalid sub-list length")

        types = [str, dict, str, str, dict]
        for i, t in enumerate(types):
            if not isinstance(sub[i], t):
                raise ValueError(f"Invalid sub-list type at position {i}")

        merged = self._merge_dicts_safe(sub[1], sub[4])

        if "syncspec" not in merged:
            raise ValueError("Missing 'syncspec' key")

        cls = self._registry.get(merged["syncspec"])
        if not cls:
            raise ValueError(f"Unknown directive: {merged['syncspec']}")

        obj = cls.model_validate(merged)
        return [sub[0], sub[1], obj, sub[2], sub[3], sub[4]]

    def _merge_dicts_safe(self, d1: dict, d2: dict) -> dict:
        if d1.keys() & d2.keys():
            raise ValueError("Conflicting keys found")
        return {**d1, **d2}