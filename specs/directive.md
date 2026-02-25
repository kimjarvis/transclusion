
Class Directive is:
- An abstract class defined in source: src/syncspec/directive.py
- A pydnatic V2 class.
- Part of the syncspec package.

## Generate a the class Directive

Use this as a guideline.

```python
from abc import ABC, abstractmethod
from pydantic import BaseModel, ConfigDict, Field

class Directive(BaseModel, ABC):
    model_config = ConfigDict(extra='forbid')

    type: str = Field(..., description="Type of syncspec directive")

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

