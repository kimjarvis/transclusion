from typing import NamedTuple, Tuple


class TextSplit(NamedTuple):
    first: str
    middle: str
    last: str


def split(text: str, head: int, front: int, back: int, tail: int) -> TextSplit:
    if head < 0 or front < 0 or back < 0 or tail < 0:
        raise ValueError("Negative values are not allowed for head, front, back, and tail.")

    lines = text.splitlines(True)
    n = len(lines)

    # Compute first part
    if head == 0:
        if n == 0:
            if front > 0:
                raise ValueError("Not enough text for front part: text is empty but front>0")
            first_part = ''
        else:
            if front > len(lines[0]):
                raise ValueError(
                    f"Not enough characters in the first line for front part: first line has {len(lines[0])} characters, but front={front}")
            first_part = lines[0][:front]
    else:
        if n < head:
            raise ValueError(f"Not enough lines for head part: text has {n} lines, but head={head}")
        first_part = ''.join(lines[:head])
        if front > 0:
            if n <= head:
                raise ValueError(
                    f"Not enough lines for front part: text has {n} lines, but head={head} and front>0 requires at least {head + 1} lines")
            if front > len(lines[head]):
                raise ValueError(
                    f"Not enough characters in line {head} for front part: line has {len(lines[head])} characters, but front={front}")
            front_part = lines[head][:front]
            if '\n' in front_part:
                raise ValueError(
                    f"Front part contains a newline character: cannot take {front} characters from line {head} because it includes a newline")
            first_part += front_part

    # Compute last part
    if tail == 0:
        if n == 0:
            if back > 0:
                raise ValueError("Not enough text for back part: text is empty but back>0")
            last_part = ''
        else:
            last_line = lines[-1]
            if back > len(last_line):
                raise ValueError(
                    f"Not enough characters in the last line for back part: last line has {len(last_line)} characters, but back={back}")
            last_part = last_line[-back:] if back > 0 else ''
    else:
        if n < tail:
            raise ValueError(f"Not enough lines for tail part: text has {n} lines, but tail={tail}")
        tail_block = ''.join(lines[n - tail:])
        if back > 0:
            if n < tail + 1:
                raise ValueError(
                    f"Not enough lines for back part: text has {n} lines, but tail={tail} and back>0 requires at least {tail + 1} lines")
            line_above = lines[n - tail - 1]
            if back > len(line_above):
                raise ValueError(
                    f"Not enough characters in line {n - tail - 1} for back part: line has {len(line_above)} characters, but back={back}")
            back_part = line_above[-back:]
            last_part = back_part + tail_block
        else:
            last_part = tail_block

    first_len = len(first_part)
    last_len = len(last_part)
    total_len = len(text)

    if first_len + last_len > total_len:
        raise ValueError("Not enough text: the first part and last part overlap or extend beyond the text")

    middle_part = text[first_len:total_len - last_len]
    return TextSplit(first_part, middle_part, last_part)