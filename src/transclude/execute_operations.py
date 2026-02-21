from typing import Any
from .operation import Operation


def execute_operations(x: list[Any], state: dict) -> list[Any]:
    result = []
    for item in x:
        if not isinstance(item, list):
            result.append(item)
            continue

        if len(item) != 6:
            raise ValueError(f"Sub-list must have 6 elements, got {len(item)}")

        # Based on example data and [a,b,c,d,e,f] clarification:
        # c (index 2) is object, d (index 3) is string
        obj_item = item[2]
        str_item = item[3]

        if not isinstance(obj_item, Operation):
            raise ValueError(f"Item at index 2 must be Operation, got {type(obj_item)}")

        if not isinstance(str_item, str):
            raise ValueError(f"Item at index 3 must be str, got {type(str_item)}")

        executed_value = obj_item.execute(str_item, state)
        changed = executed_value != str_item

        new_sublist = item + [executed_value, changed]
        result.append(new_sublist)

    return result