## Write a class Include

In source: src/transclude/operations/include.py

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
Use Literal["Include"] for Discriminator Safety.

Include class has field:

```python
    type: Literal["Include"] = Field(default="Include", init=False)
    file: Optional[str] = Field(..., description="File path to read")
    key: Optional[str] = Field(..., description="Dictionary key to read")    
    head: Optional[int] = Field(default=None, description="Number of lines from the beginning to retain")
    tail: Optional[int] = Field(default=None, description="Number of lines from the end to retain")
    front: Optional[int] = Field(default=None, description="Number of characters from the beginning to retain")
    bask: Optional[int] = Field(default=None, description="Number of characters from the end to retain")
```

Note that, the type field uses discriminator='type' in the parent class. 
Pydantic V2 requires discriminator fields to be explicitly present in input data during instantiation

Use Pydantic V2 to ensure:
- File and key are mutually exclusive parameters.  One of them must be specified.


The function split is defined in src/transclude/split.py It can be imported like this:

```python
from ..split import split

class TextSplit(NamedTuple):
    first: str
    middle: str
    last: str


def split(text: str, head: int, front: int, back: int, tail: int) -> TextSplit:
```

The phase_one method 

1. Call split to the argument string data into strings first, middle and last.
2. Return the concatenation `first + last`.  
3. Preserve original newline characters during reconstruction.

The phase_two method

1. If self.file is specified verify that the value is a file path or a symbolic link. 
2. Read the content of the file, assume a uft-8 text file into the string x.
3. If self.key is specified, verify that the value is a dictionary key in state.  Let x=state[self.key]
4. Return the concatenation first + x + last.  
5. Preserve original newline characters during reconstruction.

### Assumptions

Make these assumptions:

- Line Endings: splitlines(keepends=True) preserves newline characters during slicing.

## Write pytest to verify the functionality.

- Pytests should be in a separate file. 
- Do not define a test class.  
- Tests should be individual functions.
- Verify the error conditions.
- Create concise tests using `@pytest.mark.parametrize` 

Explicitly pass type="Include" when instantiating Source in tests.

## Explain the solution

Describe any logical inconsistencies in the function specification and suggest improvements.

Describe any assumptions that are not explicitly stated in the function specification.