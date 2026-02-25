## Write a single function to perform the task.

Source file: reassemble_document.py

Function signature:

```python
def reassemble_document(x: list[Any], open_delimiter: str="{{", close_delimiter: str="}}") -> Tuple[bool, str]
```

Expected behavior:

```python
reassemble_document(["m",["a","b","c","d","e","g","h","i",True],"n"]) == True,"m{{a}}i{{e}}n"
```

Action:

Nesting

set the value of changed to be False
Iterate through the list.
- If the item type is string append it to the output string.
- If the item type is list:
    - Raise a value error if the length of the list is not nine.
    - Append open_delimiter to the output string.
    - Raise a value error if the type of item[0] is not string.
    - Append item[0] to the output string.
    - Append close_delimiter to the output string.
    - Raise a value error if the type of item[7] is not string.
    - Append item[7] to the output string.
    - Append open_delimiter to the output string.
    - Raise a value error if the type of item[4] is not string.
    - Append item[4] to the output string.
    - Append close_delimiter to the output string.
    - Raise a value error if the type of item[8] is not bool.
    - If item[8] is True, set changed to True
- If the item type is not list or string raise a value error.

- Return the changed boolean and the output string

Value errors should have a unique information message.

## Write pytest to verify the functionality.

Pytests should be in a separate file. 
Do not define a test class.  
Tests should be individual functions.
Use `@pytest.mark.parametrize` to create consise tests.

## Explain the solution

Describe any logical inconsistencies in the function specification and suggest improvements.

Describe any assumptions which are not explicitly stated in the function specification.
