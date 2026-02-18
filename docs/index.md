# Transclusion

[ensure_balanced_parentheses](ensure_balanced_parentheses.md)

Ensures string has balanced parentheses.

```python
def ensure_balanced_parentheses(string: str, 
                                open_parentheses: str="{{", 
                                close_parentheses: str="}}") -> None
```

[parse_parentheses](parse_parentheses.md)

Parse the string into a list.

```python
def parse_parentheses(string: str, 
                      open_parentheses: str="{{", 
                      close_parentheses: str="}}") -> list
```

```python
parse_parentheses("A{{B}}C{{D}}E") == ["A", "B", "C", "D", "E"]
```

[isolate_blocks](isolate_blocks.md) 

Create sub-lists based on position in the list.  Sub-lists are always of length three.

```python
def isolate_blocks(list) -> list
```

```python
isolate_blocks(["A","B","C","D""E"]) == ["A",["B","C","D"],"E"]
```

[prcess_chunks](process_chunks.md)

Parse the first and third strings in sub-lists as a JSON, to produce python dictionaries.

```python
def process_chunks(x: list[str]) -> list[str]
```

```python
process_chunks([[
        """
            {  "name": "John Doe" } 
        """,
        "B",
        """
            {  "title": "John Doe" }
        """]]) == [[{'name': 'John Doe'}, 'B', {'title': 'John Doe'}]]
```

[validate_chunks](validate_chunks.md)

Uses Pydantic matching to verify that python dictionaries can be converted to objects.

```python
def validate_chunks(x: list[Any]) -> None:
```

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
