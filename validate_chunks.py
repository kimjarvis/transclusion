from typing import Any, Optional
from pydantic import BaseModel, ConfigDict
from filters import Begin, End, Uppercase



class ChunkValidator:
    def __init__(self):
        self._registry: dict[str, type[BaseModel]] = {}

    def register(self, type_name: str, model: type[BaseModel]):
        self._registry[type_name] = model

    def __call__(self, x: list[Any]) -> list[Any]:
        for i, item in enumerate(x):
            if not isinstance(item, list) or len(item) != 5:
                raise ValueError(f"Invalid sub-list length {len(item)} sub-list {item}")

            sub = item
            for idx, t in enumerate([str, dict, str, str, dict]):
                if not isinstance(sub[idx], t):
                    raise ValueError(f"Invalid sub-list type at position {idx}")

            models = []
            for idx in [1, 4]:
                d = sub[idx]
                cls = self._registry.get(d.get("type"))
                if not cls:
                    raise ValueError("Invalid parameter: type")
                models.append(cls.model_validate(d))

            sub.insert(2, models[0])
            sub.insert(6, models[1])
            x[i] = sub

        return x


validate_chunks = ChunkValidator()
validate_chunks.register("Begin", Begin)
validate_chunks.register("End", End)
validate_chunks.register("Uppercase", Uppercase)