## Write a class Uppercase 

In source: src/transclude/types/uppercase.py

Inherit from an abstract pydantic V2 class Operation. 

```python
from abc import ABC, abstractmethod
from pydantic import BaseModel, ConfigDict, Field

class Operation(BaseModel, ABC):
    model_config = ConfigDict(extra='forbid', discriminator='type')

    type: str = Field(..., description="Type of transclude operation")

    @abstractmethod
    def execute(self, data: str, state: dict) -> str:
        pass
```

Operation is defined in src/transclude/operation.py.  It can be imported like this:

```python
from ..operation import Operation
```


Implement the required fields.
Use Literal["Uppercase"] for Discriminator Safety.
Implement the required methods.

The execute method shall return the data converted to uppercase.

## Write pytest to verify the functionality.

- Pytests should be in a separate file. 
- Do not define a test class.  
- Tests should be individual functions.