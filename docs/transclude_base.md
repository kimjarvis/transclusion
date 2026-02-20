
Class TranscludeBase is:
- An abstract class defined in source: src/transclude/transclude_base.py
- A pydnatic V2 class.
- Part of the transclude package.

## Generate a the class TranscludeBase

Use this as a guideline.

```python
from abc import ABC, abstractmethod
from pydantic import BaseModel, ConfigDict, Field

class TranscludeBase(BaseModel, ABC):
    model_config = ConfigDict(extra='forbid')

    type: str = Field(..., description="Type of transclude operation")

    @abstractmethod
    def execute(self, data: str, state: dict) -> str:
        pass
```

- Support Pydantic V2 automatic deserialization
- The descrimintor is the type field.
- Ensure that child classes override the execute method and the type field.

