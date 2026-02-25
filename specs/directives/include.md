## Write a class Include

In source: src/syncspec/directives/include.py

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

When overridng the methods use the same parameter names, data and state.

Directive is defined in src/syncspec/directive.py.  It can be imported like this:

```python
from ..directive import Directive
```

Implement the required fields.
Use Literal["Include"] for Discriminator Safety.

Include class has field:

```python
    type: Literal["Include"] = Field(default="Include")
    file: Optional[str] = Field(description="File path to read")
    key: Optional[str] = Field(description="Dictionary key to read")    
    head: Optional[int] = Field(default=1, description="Number of lines from the head to skip")
    tail: Optional[int] = Field(default=1, description="Number of lines from the tail to skip")  
```

Use Pydantic V2 to ensure:

- File and key are mutually exclusive parameters.  One of them must be specified.
- head is optional it defaults to 1
- tail is optional it defaults to 1

The function split is defined in src/syncspec/split.py. It can be imported like this:

```python
from ..split import split
```

```python
def split(text: str, head: int, tail: int) -> TextSplit:
```

```python
from typing import NamedTuple
class TextSplit(NamedTuple):
    top: str
    middle: str
    bottom: str
```

The phase_one method 

1. Call `split(data,self.head,self.tail)` using the argument sting data.  This returns a `TextSplit` object with string fields top, middle and bottom.
2. Return the concatenation top + bottom.  
3. Preserve original newline characters during reconstruction.

The phase_two method

1. If self.file is specified verify that the value is a file path or a symbolic link. 
2. Read the content of the file, assume a uft-8 text file into the string x.
3. If self.key is specified, verify that the value is a dictionary key in state.  Let x=state[self.key]
4. Call `split(data,self.head,self.tail)` using the argument sting data.  This returns a `TextSplit` object with string fields top, middle and bottom.
5. Return the concatenation top + x + bottm.  
6. Preserve original newline characters during reconstruction.

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