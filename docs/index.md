# Transclusion

# [ensure_balanced_delimiters](ensure_balanced_delimiters.md)

Ensures string has balanced delimiters.

Function signature:

```python
def ensure_balanced_delimiters(string: str, 
                                open_delimiter: str="{{", 
                                close_delimiter: str="}}") -> None
```

Expected behaviour:

Raise an exception when delimiters are not balanced.

# [parse_delimiters](parse_delimiters.md)

Parse the string into a list.

Function signature:

```python
def parse_delimiters(string: str, 
                      open_delimiter: str="{{", 
                      close_delimiter: str="}}") -> list
```

Expected behaviour:

```python
parse_delimiters("A{{B}}C{{D}}E") == ["A", "B", "C", "D", "E"]
```

# [isolate_blocks](isolate_blocks.md) 

Create sub-lists based on position in the list.  Sub-lists are always of length three.

Function signature:

```python
def isolate_blocks(list) -> list
```

Expected behaviour:

```python
isolate_blocks(["A","B","C","D""E"]) == ["A",["B","C","D"],"E"]
```

# [prcess_chunks](process_chunks.md)

Parse the first and third strings in sub-lists as a JSON, to produce python dictionaries.

Function signature:

```python
def process_chunks(x: list[str]) -> list[Any]
```

Expected behaviour:

```python
process_chunks([[
        """
            {  "name": "John Doe" } 
        """,
        "B",
        """
            {  "title": "John Doe" }
        """]]) == [[
        """
            {  "name": "John Doe" } 
        """,
        {'name': 'John Doe'},
        'B',
        """
            {  "title": "John Doe" }
        """,    
        {'title': 'John Doe'}
        ]]
```

# [validate_chunks](validate_chunks.md)

Uses Pydantic matching to verify that python dictionaries can be converted to objects.

Function signature:

```python
def validate_chunks(x: list[Any]) -> None:
```

Expected behaviour:

```python
validate_chunks(
    [['A', {'type': 'Begin', 'source': 's', 'shift': 1}, 'B', 'C', {'type': 'End'}]]
) == [['A', 
       {'type': 'Begin', 'source': 's', 'shift': 1}, 
       Begin(type='Begin', source='s', shift=1, skip=None, add=None), 
       'B', 
       'C', 
       {'type': 'End'}, 
       End(type='End')
    ]]
```

# [filters](filters.md)

Defines classes Begin, End and Uppercase.

# [execute](execute.md)

Call the execute method of the filter objects with the string block as the argument.

Function signature:

```python
def execute(x: list[Any]) -> list[Any]
```

Expected behavior:

```python
execute([['A', 
          {'type': 'Begin', 'source': 's', 'shift': 1}, 
          Begin(type='Begin', source='s', shift=1, skip=None, add=None), 
          'B', 
          'C', 
          {'type': 'End'}, 
          End(type='End')
          ]]) ==
          [['A', 
          {'type': 'Begin', 'source': 's', 'shift': 1}, 
          Begin(type='Begin', source='s', shift=1, skip=None, add=None), 
          'B', 
          'C', 
          {'type': 'End'}, 
          End(type='End'),
          'result of execute()'
          ]]    
```

# [reconstruct](reconstruct.md)

Construct a string from a list.

Function signature:

```python
def reconstruct(x: list[Any], open_delimiter: str="{{", close_delimiter: str="}}") -> bool, str
```

Expected behavior:

```python
reconstruct(["m",["a","b","c","d","e","f","g","h",True],"n"]) == True,"m{{a}}h{{e}}n"
```
