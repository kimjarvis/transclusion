## Write a class to perform the task.

Source file: dictionaries_to_filters.py

Function signature:

```python
class ChunkValidator:
    def dictionaries_to_filters(x: list[str]) -> list[Any]:
        pass
    def register(self, filer: str, cls: Any):
        pass
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

Combine the sub-list item [1] and [4] dictionaries.  Use this function as a guide.

```python
def merge_dicts_safe(d1, d2):
    """Merge two dictionaries. Raises ValueError if keys overlap."""
    if d1.keys() & d2.keys():
        raise ValueError("Conflicting keys found")
    return {**d1, **d2}
```

- Use pydantic V2 to validate the combined dictionary.
- The key "type" must be present in the combined dictionary.
- The value of the "type" key must be present in the class registry.

Classes are registered with the register method `register(type, cls)` where type is a string and cls is the pydantic class.
The type string is used to look up the class in the class registry.  The dictionary is validated using the class.

Output a list with the object constructed from the combined dictionaries added.  
If the input list is in the form `[m,[a,b,c,d,e],n]` then b and e are both dictionaries.  
These dictionaries are used to construct object x.   
The output list shall be the list `[m,[a,b,x,c,d,e],n]`

## Write pytest to verify the functionality.

Pytests should be in a separate file.  
Do not define a test class.  Tests should be individual functions.
Verify the error conditions.

Verify valid invalid dictionary structures.  Use this as a guide:

```python
@pytest.mark.parametrize("idx, val, msg", [
    (0, 1, "Invalid sub-list type at position 0"),
    (1, "x", "Invalid sub-list type at position 1"),
    (2, 1, "Invalid sub-list type at position 2"),
    (3, 1, "Invalid sub-list type at position 3"),
    (4, "x", "Invalid sub-list type at position 4"),
])
def test_invalid_types(idx, val, msg):
    data = ["a", {}, "c", "d", {}]
    data[idx] = val
    with pytest.raises(ValueError, match=msg):
        dictionaries_to_filters([data])
```

