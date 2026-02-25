from typing import NamedTuple

class TextSplit(NamedTuple):
    top: str
    middle: str
    bottom: str

def split(text: str, head: int, tail: int) -> TextSplit:
    if head < 0 or tail < 0:
        raise ValueError("head and tail must be non-negative")

    # Normalize: ensure text ends with newline for consistent line splitting
    # Empty string is treated as a single empty line -> becomes "\n"
    needs_norm = not text.endswith('\n')
    work_text = text + '\n' if needs_norm else text

    lines = work_text.splitlines(True)
    n = len(lines)

    if head + tail > n:
        raise ValueError(f"Not enough lines: {n} available, {head + tail} requested")

    top_lines = lines[:head]
    bottom_lines = lines[-tail:] if tail > 0 else []
    middle_lines = lines[head:-tail] if tail > 0 else lines[head:]

    top = "".join(top_lines)
    middle = "".join(middle_lines)
    bottom = "".join(bottom_lines)

    # Denormalize: remove the appended newline from the last non-empty part
    if needs_norm:
        if bottom:
            bottom = bottom[:-1]
        elif middle:
            middle = middle[:-1]
        elif top:
            top = top[:-1]

    return TextSplit(top, middle, bottom)