## Write a class Source

In source: src/transclude/types/source.py

Inherit from an abstract pydantic V2 class TranscludeBase. 

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

TranscludeBase is defined in src/transclude/transclude_base.py.  It can be imported like this:

```python
from ..transclude_base import TranscludeBase
```

Implement the required fields.
Use Literal["Source"] for Discriminator Safety.
Implement the required methods.

Source class has field:

```python
    type: Literal["Source"] = Field(default="Source", init=False)
    source: str = Field(..., description="File path to source")
    head: Optional[int] = Field(description="Number of lines from the beginning to retain")
    tail: Optional[int] = Field(description="Number of lines from the end to retain")
```

Note that, the type field uses discriminator='type' in the parent class. 
Pydantic V2 requires discriminator fields to be explicitly present in input data during instantiation

Implement the execute method.

0. head and tail are optional, they both default to 0.
1. Verify that self.source is a file path or a symbolic link.
2. Read the content of the file, assume a uft-8 text file.
3. Call the file content x
4. Raise a value error with message, when head+tail is greater than the number of lines in data + 1.
5. Let the first head number of lines of data be a
6. Let the last tail number of lines of data be b
7. Return the concatinated the file content c = a + x + b.  
8. Preserve original newline characters during reconstruction.

## Write pytest to verify the functionality.

- Pytests should be in a separate file. 
- Do not define a test class.  
- Tests should be individual functions.

Explicitly pass type="Source" when instantiating Source in tests.

## Explain the solution

Describe any logical inconsistencies in the function specification and suggest improvements.

Describe any assumptions that are not explicitly stated in the function specification.