## Write a class Source

In source: src/transclude/operations/source.py

Inherit from an abstract pydantic V2 class Operation. 

```python
from abc import ABC, abstractmethod
from pydantic import BaseModel, ConfigDict, Field

class Operation(BaseModel, ABC):
    model_config = ConfigDict(extra='forbid', discriminator='type')

    type: str = Field(..., description="Type of transclude operation")

    @abstractmethod
    def phase_one(self, data: str, state: dict) -> str:
        pass

    @abstractmethod
    def phase_two(self, data: str, state: dict) -> str:
        pass
```

Operation is defined in src/transclude/operation.py.  It can be imported like this:

```python
from ..operation import Operation
```

Implement the required fields.
Use Literal["Source"] for Discriminator Safety.

Source class has field:

```python
    type: Literal["Source"] = Field(default="Source", init=False)
    file: Optional[str] = Field(..., description="File path to write")
    key: Optional[str] = Field(..., description="Dictionary key to write")    
    head: Optional[int] = Field(default=None, description="Number of lines from the beginning to retain")
    tail: Optional[int] = Field(default=None, description="Number of lines from the end to retain")
```

Note that, the type field uses discriminator='type' in the parent class. 
Pydantic V2 requires discriminator fields to be explicitly present in input data during instantiation

Use Pydantic V2 to ensure:
- File and key are mutually exclusive parameters.  One of them must be specified.

The phase_one method 

1. Remove self.head number of lines from the beginning of data.
2. Remove self.tail number of lines from the end.
3. If file is specified write the resulting string to the file specified by self.file.
4. If key is specified write the resulting string to the dictionary state `state[self.key] = data`

The phase_two method

1. Return data.

## Write pytest to verify the functionality.

- Pytests should be in a separate file. 
- Do not define a test class.  
- Tests should be individual functions.

Explicitly pass type="Source" when instantiating Source in tests.

## Explain the solution

Describe any logical inconsistencies in the function specification and suggest improvements.

Describe any assumptions that are not explicitly stated in the function specification.