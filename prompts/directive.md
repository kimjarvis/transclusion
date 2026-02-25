
Class Operation is:
- An abstract class defined in source: src/transclude/operation.py
- A pydnatic V2 class.
- Part of the transclude package.

## Generate a the class Operation

Use this as a guideline.

```python
from abc import ABC, abstractmethod
from pydantic import BaseModel, ConfigDict, Field

class Operation(BaseModel, ABC):
    model_config = ConfigDict(extra='forbid')

    type: str = Field(..., description="Type of transclude operation")

    @abstractmethod
    def phase_one(self, data: str, state: dict) -> str:
        pass

    @abstractmethod
    def phase_two(self, data: str, state: dict) -> str:
        pass

```

There are two abstract methods, phase_one and phase_two, that must be implemented by all children.

- Support Pydantic V2 automatic deserialization
- The descrimintor is the type field.
- Ensure that child classes override the execute method and the type field.

