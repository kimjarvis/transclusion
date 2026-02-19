from typing import Any
from filters import Base


def execute_filters(x: list[Any]) -> list[Any]:
    for i, item in enumerate(x):
        if isinstance(item, list):
            if len(item) != 6:
                raise ValueError(f"Sub-list at index {i} must have 6 elements.")

            obj, data = item[2], item[3]

            if not isinstance(obj, Base):
                raise TypeError(f"Item at index 2 in sub-list {i} must inherit from Base.")
            if not isinstance(data, str):
                raise TypeError(f"Item at index 3 in sub-list {i} must be a string.")

            result = obj.execute(data)
            changed = result != data

            item.append(result)
            item.append(changed)

    return x