## Write a single function to perform the task.

Check in this order:

1. Check that the delimiters in the string are not nested.
  - Raise an a ValueError "Parentheses cannot be nested"
2. Check if the delimiters in the string are balanced.
  - Raise an a ValueError "Parentheses are not matched"

Function signature:

```python
def ensure_balanced_delimiters(string: str, open_delimiter: str="{{", close_delimiter: str="}}") -> None.
```

Check in this order:

1. open_delimiter and close_delimiter must be different.
  - Raise an a ValueError "Opening and closing delimiters must be different"
2. The last character of open_delimiter cannot be the same as the first character of close_delimiter.
    - Raise an a ValueError "The last character of open_delimiter cannot be the same as the first character of close_delimiter"

## Write pytest to verify the functionality.
Pytests should be in a separate file.

Minimum valid test cases:  

ensure_balanced_delimiters("")  
ensure_balanced_delimiters("{{ }}")

A ValueError shall be raised in these cases:

ensure_balanced_delimiters("{{ {{ }}")
ensure_balanced_delimiters("{{ {{ }} }}")