from typing import Any
from .directive import Directive


def execute_phase_one(x: list[Any], state: dict) -> list[Any]:
    for i, item in enumerate(x):
        if isinstance(item, list):
            if len(item) < 6:
                raise ValueError(f"Sub-list at index {i} must have at least 6 elements")

            op_obj = item[2]
            data_str = item[3]

            if not isinstance(op_obj, Directive):
                raise ValueError(f"Item at index 2 in sub-list {i} must be an Operation instance")

            if not isinstance(data_str, str):
                raise ValueError(f"Item at index 3 in sub-list {i} must be a string")

            result = op_obj.phase_one(data_str, state)
            item.append(result)

    return x