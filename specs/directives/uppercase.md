## Write a class Uppercase 

In source: src/syncspec/directives/uppercase.py

Inherit from an abstract pydantic V2 class Directive. 

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

Directive is defined in src/syncspec/directive.py.  It can be imported like this:

```python
from ..directive import Directive
```

Implement the required fields.
Use Literal["Uppercase"] for Discriminator Safety.
Implement the required methods.

The phase_one method shall return the data.

The phase_two method shall return the data converted to uppercase.

## Write pytest to verify the functionality.

- Pytests should be in a separate file. 
- Do not define a test class.  
- Tests should be individual functions.