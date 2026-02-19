Parse a string into a list.  The list contains the string between each pair of delimiters.  
If there is no string between a pair of delimiters, the list contains an empty string.
Add an element for each pair of delimiters, even when there's no text before the first opening parenthesis or 
after the last closing parenthesis.

For each opening parenthesis, ensure a corresponding entry in the result list
When we find an opening parenthesis, we always add the text before it to the result (even if it's an empty string)

After processing all delimiters, if there is text remaining (text after the last closing parenthesis), we add it.

Return the string if there are no delimiters.


Write a single function to perform the task.

Function signature:

```python
def parse_delimiters(string: str, open_delimiter: str="{{", close_delimiter: str="}}") -> list:
    pass
```

Safely assume that the input string is valid.  That is:

- Parentheses are matched. 
- Parentheses cannot be nested.
- open_delimiter and close_delimiter are different.
- The last character of open_delimiter cannot be the same as the first character of close_delimiter.

Do not test for invalid input.

## Write pytest to verify the functionality.

Minimum valid test cases:  

parse_delimiters("A") == ["A"]  
parse_delimiters("A{{B}}C") == ["A", "B", "C"]
parse_delimiters("{{B}}C") == ["", "B", "C"]
parse_delimiters("{{B}}") == ["", "B", ""]
parse_delimiters("A{{B}}C{{D}}E") == ["A", "B", "C", "D", "E"]
parse_delimiters("A{{B}}{{D}}E") == ["A", "B", "", "D", "E"]
parse_delimiters("A{{}}C{{}}") == ["A", "", "C", "", ""]