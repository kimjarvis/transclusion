from typing import Any, Tuple


def reassemble_document(x: list[Any], open_delimiter: str = "{{", close_delimiter: str = "}}") -> Tuple[bool, str]:
    changed = False
    output = []

    for item in x:
        if isinstance(item, str):
            output.append(item)
        elif isinstance(item, list):
            if len(item) != 9:
                raise ValueError("List length must be 9")

            output.append(open_delimiter)
            if not isinstance(item[0], str):
                raise ValueError("Index 0 must be string")
            output.append(item[0])
            output.append(close_delimiter)

            if not isinstance(item[7], str):
                raise ValueError("Index 7 must be string")
            output.append(item[7])

            output.append(open_delimiter)
            if not isinstance(item[4], str):
                raise ValueError("Index 4 must be string")
            output.append(item[4])
            output.append(close_delimiter)

            if not isinstance(item[8], bool):
                raise ValueError("Index 8 must be bool")
            if item[8]:
                changed = True
        else:
            raise ValueError("Invalid item type")

    return changed, "".join(output)