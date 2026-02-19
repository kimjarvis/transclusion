## Write a single function to perform the task.

In source file: `process_chunks.py`

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

Action:

The argument is list with items of type string or type list.

Iterate through the list processing the items with type list.  We refer to these items as sub-lists.  Items of type string are passed through to the output list unchanged.

Each sub-list will have three elements of type string. 

Check in this order:

1. Raise a ValueError if the number of items in a sub-list is not 3 with message "Invalid sub-list length".
2. Raise a ValueError if list items are neither strings or lists with message "Invalid item type"
3. Raise a ValueError if the sub-list items are not all of type string with message "Invalid list item".

Let `[x,y,z]` represent the sub-list in list `[m,[x,y,z],n]`] 

Wrap he first and third strings in the sub-list, x and z in curly braces. 
For example: '"type": "Uppercase"' becomes '{ "type": "Uppercase" }'
Parse these wrapped strings as a JSON, to produce python dictionaries, a and b.

Return the sub-list with the dictionaries in this order:  

`[m,[x,a,y,z,b],n]`

- Raise a ValueError if the parsing the json fails with a message "Failed to parse JSON".


## Write pytest to verify the functionality.

Pytests should be in a separate file. 
Do not define a test class.  
Tests should be individual functions.

assert process_chunks(['A'])==['A']

process_chunks([5]) raise ValueError Invalid item type

process_chunks([['A']]) raise ValueError Invalid sub-list length

process_chunks([['A',3,'C']]) raise ValueError Invalid list item

process_chunks([['A','B','C']]) raise ValueError Failed to parse json

process_chunks([["""

{  "name": "John Doe",  "email": "john@example.com",  "age": 30,  "active": true,  "roles": ["admin", "user"],  "address": {    "street": "123 Main St",    "city": "New York",    "country": "USA"  },  "projects": [    {"id": 1, "name": "Website Redesign"},    {"id": 2, "name": "Mobile App"}  ] }

""","B","""

{  "title": "John Doe" }

"""]]) succeeds because both the first and third items in the sub-list are valid json strings.

The function returns 

["""

{  "name": "John Doe",  "email": "john@example.com",  "age": 30,  "active": true,  "roles": ["admin", "user"],  "address": {    "street": "123 Main St",    "city": "New York",    "country": "USA"  },  "projects": [    {"id": 1, "name": "Website Redesign"},    {"id": 2, "name": "Mobile App"}  ] }

""",
{
    "name": "John Doe",
    "email": "john@example.com",
    "age": 30,
    "active": True,
    "roles": ["admin", "user"],
    "address": {
        "street": "123 Main St",
        "city": "New York",
        "country": "USA"
    },
    "projects": [
        {"id": 1, "name": "Website Redesign"},
        {"id": 2, "name": "Mobile App"}
    ]
},"B","""

{  "title": "John Doe" }

""",
{"title": "John Doe"}]
