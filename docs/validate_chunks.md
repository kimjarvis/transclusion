## Write a single function to perform the task.

Function signature:

```python
def validate_chunks(x: list[str]) -> list[Any]
```

Action:

The argument is list with items of type string or type list.

Iterate through the list processing the items with type list. 
We refer to these items as sub-lists. 
Items with type string should be ignored.    

1. Raise a ValueError if the item is not a string or a list ith message "Invalid type".

Each sub-list will have five elements. 

Check in this order:

1. Raise a ValueError if the number of items in a sub-list is not 5 with message "Invalid sub-list length".
2. Raise a ValueError if the sub-list item [0] is not of type string with message "Invalid sub-list type at position 0".
3. Raise a ValueError if the sub-list item [1] is not of type dictionary with message "Invalid sub-list type  at position 1".
4. Raise a ValueError if the sub-list item [2] is not of type string with message "Invalid sub-list type  at position 2".
5. Raise a ValueError if the sub-list item [3] is not of type string with message "Invalid sub-list type  at position 3".
6. Raise a ValueError if the sub-list item [4] is not of type dictionary with message "Invalid sub-list type  at position 4".

Use pydantic V2 to validate the sub-list item [1] and [4] dictionaries.  If `type=="Begin"` then the dictionary has these fields:

```
{
    type: str,
    source: str,
    shift: Optional[int],
    skip: Optional[int],
    add: Optoinal[int],
}
```

Import pydantic classes Begin and End from filters.py.

Declare `class Begin(BaseModel)`  to validate this dictionary.

If `type=="End"` then the dictionary has these fields:

```
{
    type: str,
 }
```

Declare `End(BaseModel)` to validate this dictionary.

When the type is neither "Begin" or "End" raise a ValueError with message "Invalid parameter: type"

This example should be valid, no error should be raised.

```
validate_chunks(
['{"type": "Begin", "source": "example", "shift": 4, "skip": 1, "add": 1}',
{
    "type": "Begin",
    "source": "example",
    "shift": 4,
    "skip": 1,
    "add": 1
},"B",'{"type": "End"}',{"type": "End"}]
```

Ensure that dictionaries are valid.  They can only contain keys that are present in the schema.  Use the Pydantic V2 construct:

```python
    model_config = ConfigDict(extra='forbid')
```

Output a list with the objects constructed from the dictionaries added.  If the input list is in the form `[m,[a,b,c,d,e],n]` then b and e are both dictionaries.  These dictionaries are used to construct objects x and y.   The output list shall be the list `[m,[a,b,x,c,d,e,y],n]`

Register the pydantic classes with validate_chunks.  Do not refer to them explicitly within the function.
Begin and End should be registered with validate_chunks.
Register `"End",End` with validate_chunks to cause dictionaries with `type=="End"` to be validated using class End.

## Write pytest to verify the functionality.

Pytests should be in a separate file.  

Verify the error conditions.

Verify valid invalid dictionary structures.

