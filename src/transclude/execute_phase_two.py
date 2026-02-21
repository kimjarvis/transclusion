from typing import Any
from .operation import Operation


def execute_phase_two(x: list[Any], state: dict) -> list[Any]:
    for i, item in enumerate(x):
        if isinstance(item, list):
            if len(item) != 7:
                raise ValueError(f"Sub-list at index {i} must have 7 elements, got {len(item)}")

            op_obj = item[2]
            input_str = item[6]

            if not isinstance(op_obj, Operation):
                raise ValueError(f"Item at index 2 in sub-list {i} must be an Operation instance")
            if not isinstance(input_str, str):
                raise ValueError(f"Item at index 6 in sub-list {i} must be a string")

            result = op_obj.phase_two(input_str, state)
            changed = result != item[3]

            item.append(result)
            item.append(changed)

    return x