## Write a single function to perform the task.

Function signature:

```python
def validate_chunks(x: list[str]) -> None
```

Action:

The argument is list with items of type string or type list.

Iterate through the list processing the items with type list.  We refer to these items as sub-lists.  

Each sub-list will have three elements. Let `[[x,y,z]]` represent the list with one sub-list. 

Check in this order:

1. Raise a ValueError if the number of items in a sub-list is not 3 with message "Invalid sub-list length".
2. Raise a ValueError if the sub-list item [0] is not of type dictionary with message "Invalid item type".
3. Raise a ValueError if the sub-list item [1] is not of type string with message "Invalid item type".
4. Raise a ValueError if the sub-list item [2] is not of type dictionary with message "Invalid item type".

Use pydantic V2 to validate the sub-list item [0] and [2] dictionaries.  If type=="Begin" then the dictionary has these fields:

```
{
    type: str,
    source: str,
    shift: Optional[int],
    skip: Optional[int],
    add: Optoinal[int],
}
```

If type=="End" then the dictionary has these fields:

```
{
    type: str,
 }
```

Otherwise raise a ValueError with message "Invalid parameter: type"

This example should be valid, no error should be raised.

```
validae_chunks(
[{
    "type": "Begin",
    "source": "example",
    "shift": 4,
    "skip": 1,
    "add": 1
},"B",{"type": "End"}]

```

Ensure that dictionaries are valid.  They can only contain keys that are present in the schema.  Use the Pydantic V2 construct:

```python
    model_config = ConfigDict(extra='forbid')
```



## Write pytest to verify the functionality.

Pytests should be in a separate file.  

Verify the error conditions.

Verify valid invalid dictionary structures.
