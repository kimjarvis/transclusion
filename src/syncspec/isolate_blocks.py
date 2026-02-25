def isolate_blocks(list) -> list:
    if len(list) % 4 != 1:
        raise ValueError("Invalid blocks")
    if not all(isinstance(item, str) for item in list):
        raise ValueError("Invalid items")

    result = [list[0]]
    i = 1
    while i < len(list):
        result.append(list[i:i+3])
        i += 3
        if i < len(list):
            result.append(list[i])
            i += 1
    return result