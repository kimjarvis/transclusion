from typing import Any, List


class Base:
    def execute(self, data: str) -> str:
        pass


def execute(x: List[Any]) -> List[Any]:
    types = [str, dict, Base, str, str, dict, Base]
    for i, item in enumerate(x):
        if isinstance(item, list):
            if len(item) != 7:
                raise ValueError("Invalid sub-list length")
            for idx, t in enumerate(types):
                if not isinstance(item[idx], t):
                    raise ValueError(f"Invalid sub-list type at position {idx}")

            base_obj, input_str = item[2], item[3]
            result = base_obj.execute(input_str)
            changed = result != input_str
            item.extend([result, changed])
    return x