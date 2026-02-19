import json
from typing import Any


def process_chunks(x: list[str]) -> list[Any]:
    result = []
    for item in x:
        if isinstance(item, str):
            result.append(item)
        elif isinstance(item, list):
            if len(item) != 3:
                raise ValueError("Invalid sub-list length")
            if not all(isinstance(i, str) for i in item):
                raise ValueError("Invalid list item")

            x_str, y_str, z_str = item

            def parse_wrapped(s: str) -> dict:
                stripped = s.strip()
                if not (stripped.startswith('{') and stripped.endswith('}')):
                    stripped = '{' + stripped + '}'
                try:
                    return json.loads(stripped)
                except json.JSONDecodeError:
                    raise ValueError("Failed to parse JSON")

            parsed_x = parse_wrapped(x_str)
            parsed_z = parse_wrapped(z_str)
            result.append([x_str, parsed_x, y_str, z_str, parsed_z])
        else:
            raise ValueError("Invalid item type")
    return result