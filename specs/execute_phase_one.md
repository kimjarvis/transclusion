## Write a single function to perform the task.

Source file: src/syncspec/execute_phase_one.py

Function signature:

```python
def execute_phase_one(x: list[Any], state: dict) -> list[Any]:
```

Expected behavior:

```python
execute_phase_one([['A', 
          {'type': 'Begin', 'source': 's', 'shift': 1}, 
          Begin(type='Begin', source='s', shift=1, skip=None, add=None), 
          'B', 
          'C', 
          {'xtype': 'End'}, 
          ]]) ==
          [['A', 
          {'type': 'Begin', 'source': 's', 'shift': 1}, 
          Begin(type='Begin', source='s', shift=1, skip=None, add=None), 
          'B', 
          'C', 
          {'xtype': 'End'}, 
          'result of execute_phase_one()',
          ]]    
```

Action:

The argument is list with items of type string or type list.

Iterate through the list processing the items with type list. We refer to these items as sub-lists. Each sub-list will have six elements. 

item [3] is an object.  
item [4] is a string.

Verify that these items are of the correct type issue value error with a message if they are not.

The item[3] is an object of a pydantic V2 class whose parent class is defined in src/syncspec/directive.py as follows:

```python
from abc import ABC, abstractmethod
from pydantic import BaseModel, ConfigDict, Field

class Directive(BaseModel, ABC):
    model_config = ConfigDict(extra='forbid', discriminator='type')

    type: str = Field(..., description="Type of syncspec directive")

    @abstractmethod
    def phase_one(self, data: str, state: dict) -> str:
        pass

    @abstractmethod
    def phase_two(self, data: str, state: dict) -> str:
        pass
```

Call the phase_one() method of the object with the string as the argument.  Like this:

item[3].phase_one(item[4], state)

- state is the dictionary passed as a parameter to directive.


Output the input list with the result of phase_one() added to the sub-list.  
If the input list is in the form `[m,[a,b,c,d,e,f],n]` then c is an object of a type that inherits from Directive and d is a string.  
Call the output of `c.phase_one(d, state)` h. 
The output list shall be the list `[m,[a,b,c,d,e,f,h],n]`

## Write pytest to verify the functionality.

Pytests should be in a separate file.  
Do not use a class, each test should be a function.

- Verify the error conditions.
- Verify valid invalid dictionary structures.

