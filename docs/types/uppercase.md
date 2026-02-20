## Write a class Uppercase 

In source: src/transclude/types/uppercase.py

Inherit from an abstract pydantic V2 class TranscludeBase which is defined in src/transclude/transclude_base.py 

```python
from abc import ABC, abstractmethod
from pydantic import BaseModel, ConfigDict, Field

class TranscludeBase(BaseModel, ABC):
    model_config = ConfigDict(extra='forbid', discriminator='type')

    type: str = Field(..., description="Type of transclude operation")

    @abstractmethod
    def execute(self, data: str, state: dict) -> str:
        pass
```

Implement the required fields.
Use Literal["Uppercase"] for Discriminator Safety.
Implement the required methods.

The execute method shall return the data converted to uppercase.

## Explain the solution

Describe any logical inconsistencies in the function specification and suggest improvements.

Describe any assumptions which are not explicitly stated in the function specification.