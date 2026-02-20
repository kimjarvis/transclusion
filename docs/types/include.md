## Write a single function to perform the task.

Source file: include.py

Declare class Include

```python
from pathlib import Path
from pydantic import Field
from src.transclude.filters import Base


class Include(Base):
    type: str = Field(..., description="Include type")
    source: str = Field(..., alias="file", description="File path to include")
```

Implement the execute method.

1. Verify that self.source is a file path or a symbolic link.
2. Read the content of the file, assume a uft-8 text file.
3. Return the content of the file.

### Base class

```python
from abc import ABC, abstractmethod
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field

class Base(BaseModel, ABC):
    model_config = ConfigDict(extra='forbid')

    @abstractmethod
    def execute(self, data: str, state: dict) -> str:
        pass
```

## Write pytest to verify the functionality.

- Pytests should be in a separate file. 
- Do not define a test class.  
- Tests should be individual functions.

## Explain the solution

Describe any logical inconsistencies in the function specification and suggest improvements.

Describe any assumptions that are not explicitly stated in the function specification.