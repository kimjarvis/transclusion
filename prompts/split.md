## Write a single function to perform the task.

Source file: src/transclude/split.py

Function signature:

```python
def split(lines: list(str), head: int, front: int, back: int, tail: int) -> Tuple[list[str],list[str],list[str]]
```

Expected behavior:

The list of lines is split into three parts.

Return
1. A list containing the first "head" items in lines and an additional item.  This item is a substring containing the first "front" characters of the next item.
2. A list containing the last "tail" item in lines with an item added at the front.  This item is a substring containing the last "back" characters of the previous item.
3. A list containing the middle items in lines. 

Raise value errors with a message:
- When there are not enough lines to perform the split. 
- When there are not enough characters in the line to extract the front and back.
- When the messages head and front overlap the back and the tail. 

## Write pytest to verify the functionality.

- Ensure that the strings created by concatinating the first, middle and last lists are equal to the original lines.

Pytests should be in a separate file.  
Do not use a class, each test should be a function.

- Verify the error conditions.
- Create concise tests using `@pytest.mark.parametrize` 

## Explain the solution

Describe any logical inconsistencies in the function specification and suggest improvements.

Describe any assumptions that are not explicitly stated in the function specification.
