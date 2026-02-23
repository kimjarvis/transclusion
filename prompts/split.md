# Write a single function to perform the task.

Function signature:

```python
def split(text: str, head: int, front: int, back: int, tail: int) -> Tuple[str,str,str]
```

Use dataclasses or named tuples for the return type to make the result self-documenting:

```python
from typing import NamedTuple
class TextSplit(NamedTuple):
    first: str
    middle: str
    last: str
```

Source file: src/transclude/split.py

# Expected behavior:

The string text is split into three parts: first, middle, and last and returned in a tuple.
When head is not zero, the first part contains the first "head" lines of text followed by "front" characters from the next line.
When head is zero, the first part contains the first "front" characters from the first line.
The middle part contains the text between the first part and the last part.
When head is zero and tail is zero and front/back are on the same line, middle is what's between them on that line.
When tail is not zero, the last part contains the last "tail" lines of text preceded by "back" characters from the previous line.
When tail is zero, the last part contains the last "back" characters from the last line.
The returned first + middle + last parts should always be equal to the original text.

# Examples

```python
"line1\nl","ine2","\nline3\n" == split("line1\nline2\nline3\n",1,1,1,1) 
```

```python
"", "a\nb\n", "" == split("a\nb\n",0,0,0,0)
```
  
```python
"a\n", "", "b\n" == split("a\nb\n",1,0,0,1) 
``` 

Raise a value error with a message:
- There is not enough text to perform the split.  Each value error should have an informative message explaining why the split cannot be performed.
- Negative values are not allowed for head, front, back, and tail.
- When head > 0 the additional characters that it adds to the first part must not contain a new line character.
- When tail > 0 the additional characters that it adds to the last part must not contain a new line character, other than in the last character position.

## Assumptions

Make the following assumptions:

- Newline Preservation: splitlines(True) is used to ensure concatenation restores original newlines.
- Character Count: front and back counts include newline characters if they fall within the range.
- Use conditional slicing (if back > 0) to avoid edge case where [:-0] results in an empty string, not the full string.
- The Source fields are Optional[int], but split expects int. Assume None implies 0 

## Write pytest to verify the functionality.

- Pytests should be in a separate file.  
- Do not use a class, each test should be a function.
- Verify the error conditions.
- Create concise tests using `@pytest.mark.parametrize` 

## Explain the solution

Describe any logical inconsistencies in the function specification and suggest improvements.

Describe any assumptions that are not explicitly stated in the function specification.
