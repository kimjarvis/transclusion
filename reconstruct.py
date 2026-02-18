from typing import Any

def reconstruct(x: list[Any], open_parentheses: str="{{", close_parentheses: str="}}") -> tuple[bool, str]:
    changed, out = False, ""
    for item in x:
        if isinstance(item, str): out += item
        elif isinstance(item, list):
            if len(item) != 9: raise ValueError()
            out += open_parentheses
            if not isinstance(item[0], str): raise ValueError()
            out += item[0]
            out += close_parentheses
            if not isinstance(item[7], str): raise ValueError()
            out += item[7]
            out += open_parentheses
            if not isinstance(item[4], str): raise ValueError()
            out += item[4]
            out += close_parentheses
            if not isinstance(item[8], bool): raise ValueError()
            if item[8]: changed = True
        else: raise ValueError()
    return changed, out