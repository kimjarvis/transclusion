def parse_delimiters(string: str, open_delimiter: str = "{{", close_delimiter: str = "}}") -> list:
    """
    Parse a string by splitting at each pair of delimiters.

    Args:
        string: The input string to parse
        open_delimiter: The opening parenthesis delimiter
        close_delimiter: The closing parenthesis delimiter

    Returns:
        A list containing the text between each pair of delimiters,
        including empty strings where appropriate
    """
    result = []
    current_pos = 0
    len_open = len(open_delimiter)
    len_close = len(close_delimiter)

    # If there are no delimiters in the string, return the string as a single element
    if open_delimiter not in string and close_delimiter not in string:
        return [string]

    while current_pos < len(string):
        # Find the next opening parenthesis
        open_pos = string.find(open_delimiter, current_pos)

        if open_pos == -1:
            # No more opening delimiters, add remaining text and break
            result.append(string[current_pos:])
            break

        # Add text before the opening parenthesis
        result.append(string[current_pos:open_pos])

        # Find the closing parenthesis for this opening
        close_pos = string.find(close_delimiter, open_pos + len_open)

        # Extract text between delimiters
        between_text = string[open_pos + len_open:close_pos]
        result.append(between_text)

        # Move current position past the closing parenthesis
        current_pos = close_pos + len_close

    # If we've processed everything and there's no text after the last closing parenthesis,
    # we need to add an empty string for the trailing text
    if current_pos == len(string):
        result.append("")

    return result