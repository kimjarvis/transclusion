# delimiters_checker.py

def ensure_balanced_delimiters(string: str, open_delimiter: str = "{{", close_delimiter: str = "}}") -> None:
    """
    Check that delimiters in a string are balanced and not nested.

    Args:
        string: The string to check
        open_delimiter: The opening delimiters string (default: "{{")
        close_delimiter: The closing delimiters string (default: "}}")

    Raises:
        ValueError: If validation fails with specific error messages
    """
    # Check if opening and closing delimiters are different
    if open_delimiter == close_delimiter:
        raise ValueError("Opening and closing delimiters must be different")

    # Check if the last character of open_delimiter equals the first character of close_delimiter
    if open_delimiter[-1] == close_delimiter[0]:
        raise ValueError(
            "The last character of open_delimiter cannot be the same as the first character of close_delimiter")

    open_len = len(open_delimiter)
    close_len = len(close_delimiter)

    i = 0
    found_open = False

    while i < len(string):
        # Check for opening delimiters
        if string[i:i + open_len] == open_delimiter:
            if found_open:
                raise ValueError("Parentheses cannot be nested")
            found_open = True
            i += open_len

        # Check for closing delimiters
        elif string[i:i + close_len] == close_delimiter:
            if not found_open:
                raise ValueError("Parentheses are not matched")
            found_open = False
            i += close_len
        else:
            i += 1

    # Check if there's an unclosed opening parenthesis
    if found_open:
        raise ValueError("Parentheses are not matched")