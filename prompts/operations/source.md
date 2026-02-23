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

When overridng the methods use the same parameter names, data and state.

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
    head: Optional[int] = Field(default=None, description="Number of lines from the beginning to skip")
    tail: Optional[int] = Field(default=None, description="Number of lines from the end to skip")
    strip: Optional[str] = Field(default=None, description="Stip characters from the beginning and end")
    lstrip: Optional[str] = Field(default=None, description="Stip characters from the beginning")
    rstrip: Optional[str] = Field(default=None, description="Stip characters from the end")
```

Note that, the type field uses discriminator='type' in the parent class. 
Pydantic V2 requires discriminator fields to be explicitly present in input data during instantiation

Use Pydantic V2 to ensure:
- File and key are mutually exclusive parameters.  One of them must be specified.

The phase_one method 

1. Trim self.head number of lines from the beginning of the argument "data" and pass to the next step.
2. Trim self.tail number of lines from the end and pass to the next step.
3. Run strip() on the trimmed string and pass to the next step.  If self.strip=="" then run strip().
4. Run lstrip() on the trimmed string and pass to the next step.  If self.strip=="" then run lstrip().
5. Run rstrip() on the trimmed string and pass to the next step.  If self.strip=="" then run rstrip().
3. If file is specified write the trimmed string to the file specified by self.file.
4. If key is specified write the trimmed string to the dictionary state `state[self.key] = trimmed`
5. Return the value of the argument string data unchanged.

The phase_two method

1. Return the value of the argument string data unchanged.

## Assumptions

Make these assumptions:

- Line Endings: splitlines(keepends=True) preserves newline characters during slicing.
- Strip Behavior: strip methods treat the argument as a set of characters to remove, not a substring.
- Zero Values: head=0 or tail=0 are treated as falsy (no operation).

## Write pytest to verify the functionality.

- Pytests should be in a separate file. 
- Do not define a test class.  
- Tests should be individual functions.

Explicitly pass type="Source" when instantiating Source in tests.

## Explain the solution

Describe any logical inconsistencies in the function specification and suggest improvements.

Describe any assumptions that are not explicitly stated in the function specification.