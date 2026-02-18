## Write a single function to perform the task.

Function signature:

```python
def reconstruct(x: list[Any], open_parentheses: str="{{", close_parentheses: str="}}") -> bool, str
```

Expected behavior:

```python
reconstruct(["m",["a","b","c","d","e","f","g","h",True],"n"]) == True,"m{{a}}h{{e}}n"
```

Action:

set the value of changed to be False
Iterate through the list.  
- If the item type is string append it to the output string.
- If the item type is list:
  - Raise a value error if the length of the list is not nine.
  - Append open_parentheses to the output string.
  - Raise a value error if the type of item[0] is not string.
  - Append item[0] to the output string.
  - Append close_parentheses to the output string.
  - Raise a value error if the type of item[7] is not string.
  - Append item[7] to the output string.
  - Append open_parentheses to the output string.
  - Raise a value error if the type of item[4] is not string.
  - Append item[4] to the output string.
  - Append close_parentheses to the output string.
  - Raise a value error if the type of item[8] is not bool.
  - If item[8] is True, set changed to True
- If the item type is not list or string raise a value error.
Return the changed boolean and the output string
