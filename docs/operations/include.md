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
    head: Optional[int] = Field(description="Number of lines from the beginning to retain")
    tail: Optional[int] = Field(description="Number of lines from the end to retain")
```

Note that, the type field uses discriminator='type' in the parent class. 
Pydantic V2 requires discriminator fields to be explicitly present in input data during instantiation

Use Pydantic V2 to ensure:
- File and key are mutually exclusive parameters.  One of them must be specified.

The phase_one method 

1. head and tail are optional, they both default to 0.
2. Raise a value error with message, when head+tail is greater than the number of lines in data.
3. Let the first head number of lines of data be a
4. Let the last tail number of lines of data be b
5. Return the concatenation a + b.  
6. Preserve original newline characters during reconstruction.

When head=0,tail=0,data="line1\nline2\nline3\nline4\n"
Return data=""
When head=1,tail=1,data="line1\nline2\nline3\nline4\n"
Return data="line1\nline4\n"
When head=2,tail=2,data="line1\nline2\nline3\nline4\n"
Return data="line1\nline2\nline3\nline4\n"

The phase_two method

1. If self.file is specified verify that the value is a file path or a symbolic link. 
2. Read the content of the file, assume a uft-8 text file into the string x.
3. If self.key is specified, verify that the value is a dictionary key in state.  Let x=state[self.key]
4. Let the first head number of lines of data be a
5. Let the last tail number of lines of data be b
6. Return the concatenation a + x + b.  
7. Preserve original newline characters during reconstruction.

When head=0,tail=0,data="line1\nline2\nline3\nline4\n",file content="xxx"
Return data="xxx"
When head=1,tail=1,data="line1\nline2\nline3\nline4\n",file content="xxx"
Return data="line1\nxxxline4\n"
When head=2,tail=2,data="line1\nline2\nline3\nline4\n",file content="xxx"
Return data="line1\nline2\nxxxline3\nline4\n"

## Write pytest to verify the functionality.

- Pytests should be in a separate file. 
- Do not define a test class.  
- Tests should be individual functions.

Explicitly pass type="Include" when instantiating Include in tests.

## Explain the solution

Describe any logical inconsistencies in the function specification and suggest improvements.

Describe any assumptions that are not explicitly stated in the function specification.