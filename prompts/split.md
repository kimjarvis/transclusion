# Write a single function to perform the task.

Function signature:

```python
def split(text: str, head: int, tail: int) -> TextSplit
```

- Negative values are not allowed for head and tail.
- There are no defaults.

Use dataclasses or named tuples for the return type to make the result self-documenting:

```python
from typing import NamedTuple
class TextSplit(NamedTuple):
    top: str
    middle: str
    bottom: str
```

Source file: src/transclude/split.py

# Expected behavior:

The string text is split into three parts: top, middle and bottom and returned.

Normalization of text: If the last character of text is not a new line character then a new line character is appended.

The top part contains the first head lines of text.  When head is zero, top is an empty string.  When head is not empty the last character must be a newline character.

The middle part contains the text between the top part and the bottom part. 

The bottom part contains the last tail lines of text. When tail is zero, bottom is an empty string. When bottom part is not empty the last character must be a newline character.

The top, middle and bottom parts cannot overlap.

The Normalization is removed before the text is returned.  If the last character of the original text is not a new line character then the text will have been normalized. In this case,  The last character of bottom , which will be a new line character, is removed. Or if bottom is the empty string then the last character of middle, which will be a ne line character, is removed or if bottom and middle are empty strings then the last character of top, which will be a new line character, is removed.

The concatenation of the returned top + middle + bottom is equal to the input text.  

Empty input is treated as a single empty line.

# Examples

```python
    split("line1\nline2\nline3\n",1,1) =="line1\n",
                                                            "line2\n",
                                                            "line3\n",
```

```python
    split("line1\nline2\nline3",1,1) =="line1\n",
                                                            "line2\n",
                                                            "line3",
```

```python
                    split("line1\nline3\n",1,1) =="line1\n",
                                                            "",
                                                            "line3\n",
```

```python
                    split("a\nb\n",0,0) == "",
                                                        "a\nb\n"
                                                        "",
```

```python
                    split("a\nb\n",1,0) == "a\n", 
                                                         "b\n", 
                                                         ""
```

```python
                    split("line\n",0,0) == "", 
                                                         "line\n", 
                                                         ""
```

```python
                    split("ab\ncd",1,1) == "ab\n","","cd"
```

```python
                    split("abcd",1,0) == "abcd","",""
```

```python
                    split("abcd",0,0) == "","abcd",""
```

```python
                    split("ab\ncd",1,0) == "ab\n","cd",""
```

```python
                    split("ab\ncd\n",1,1) == "ab\n","","cd\n"
```

```python
                    split("ab\ncd\n",2,0) == "ab\ncd\n", "", ""
```

```python
                    split("",0,0) == "", "", ""
```

# Error conditions

Raise a value error with a message:

- There is not enough lines of text to perform the split.  Each value error should have an informative message explaining why the split cannot be performed.

## Example errors

```python
split("abcd\n",1,1)
split("ab\ncd\n",2,1)
```

## Assumptions

Make the following assumptions:

- Newline Preservation: splitlines(True) is used to ensure concatenation restores original newlines.
- Only new line characters are supported `\n`.  

## Write pytest to verify the functionality.

- Pytests should be in a separate file.  
- Do not use a class, each test should be a function.
- Verify the error conditions.
- Create concise tests using `@pytest.mark.parametrize` 

## Explain the solution

Describe any logical inconsistencies in the function specification and suggest improvements.

Describe any assumptions that are not explicitly stated in the function specification.
