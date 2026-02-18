
Modify these classes to inherit from abstract class Base.

Each class must have an execute method.

Pydantic v2 classes inherit model_config from parent classes, so move this to the base class.

Execute method signature:

```python
def execute(self, data: str) -> str:
    pass
```

```python
from typing import Any, Optional
from pydantic import BaseModel, ConfigDict

class Uppercase(BaseModel):
    model_config = ConfigDict(extra='forbid')
    type: str

class Begin(BaseModel):
    model_config = ConfigDict(extra='forbid')
    type: str
    source: str
    shift: Optional[int] = None
    skip: Optional[int] = None
    add: Optional[int] = None

class End(BaseModel):
    model_config = ConfigDict(extra='forbid')
    type: str
```