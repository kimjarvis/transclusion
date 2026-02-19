from typing import Any, Tuple, List


def reconstruct(x: List[Any], open_delimiter: str = "{{", close_delimiter: str = "}}") -> Tuple[bool, str]:
    changed = False
    output = []

    for item in x:
        if isinstance(item, str):
            output.append(item)
        elif isinstance(item, list):
            if len(item) != 8:
                raise ValueError("Inner list length must be exactly 8")

            output.append(open_delimiter)

            if not isinstance(item[0], str):
                raise ValueError("Item at index 0 must be a string")
            output.append(item[0])

            output.append(close_delimiter)

            if not isinstance(item[6], str):
                raise ValueError("Item at index 6 must be a string")
            output.append(item[6])

            output.append(open_delimiter)

            if not isinstance(item[4], str):
                raise ValueError("Item at index 4 must be a string")
            output.append(item[4])

            output.append(close_delimiter)

            if not isinstance(item[7], bool):
                raise ValueError("Item at index 7 must be a boolean")
            if item[7]:
                changed = True
        else:
            raise ValueError("Top-level items must be string or list")

    return changed, "".join(output)