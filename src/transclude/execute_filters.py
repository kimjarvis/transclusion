from typing import Any
from .transclude_base import TranscludeBase


def execute_filters(x: list[Any], state: dict) -> list[Any]:
    result = []
    for item in x:
        if isinstance(item, list):
            if len(item) != 6:
                raise ValueError("Sub-list must have exactly 6 elements")

            filter_obj = item[2]
            data_str = item[3]

            if not isinstance(filter_obj, TranscludeBase):
                raise TypeError(f"{type(filter_obj)} Item  at index 2 must be an instance of TranscludeBase")
            if not isinstance(data_str, str):
                raise TypeError(f"{type(filter_obj)} Item at index 3 must be a string")

            output = filter_obj.execute(data_str, state)
            changed = (output != data_str)

            item.append(output)
            item.append(changed)
            result.append(item)
        else:
            result.append(item)
    return result