# solution.py
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
            try:
                a = json.loads(item[0])
            except Exception:
                raise ValueError("Failed to parse JSON")
            try:
                b = json.loads(item[2])
            except Exception:
                raise ValueError("Failed to parse JSON")
            result.append([item[0], a, item[1], item[2], b])
        else:
            raise ValueError("Invalid item type")
    return result