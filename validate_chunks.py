from typing import Any, List, Optional
from pydantic import BaseModel, ConfigDict, ValidationError
from filters import Begin, End, Uppercase


def validate_chunks(x: List[Any]) -> List[Any]:
    result = []
    for item in x:
        if isinstance(item, str):
            result.append(item)
        elif isinstance(item, list):
            if len(item) != 5:
                raise ValueError("Invalid sub-list length")

            types = [str, dict, str, str, dict]
            for i, t in enumerate(types):
                if not isinstance(item[i], t):
                    raise ValueError(f"Invalid sub-list type at position {i}")

            objs = []
            for idx in [1, 4]:
                d = item[idx]
                try:
                    model_cls = validate_chunks.registry.get(d.get('type'))
                    if not model_cls:
                        raise ValueError(f"Unknown type {d.get('type')}")
                    objs.append(model_cls(**d))
                except (ValidationError, ValueError) as e:
                    raise ValueError(str(e))

            new_sub = [item[0], item[1], objs[0], item[2], item[3], item[4], objs[1]]
            result.append(new_sub)
        else:
            raise ValueError("Invalid type")
    return result


validate_chunks.registry = {}
validate_chunks.registry["Begin"] = Begin
validate_chunks.registry["End"] = End
validate_chunks.registry["Uppercase"] = Uppercase