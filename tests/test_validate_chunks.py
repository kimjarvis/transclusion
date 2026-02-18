import sys
import types
import pytest
from typing import Optional
from pydantic import BaseModel, ConfigDict

# Mock filters module
filters = types.ModuleType('filters')

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

class Uppercase(BaseModel):
    model_config = ConfigDict(extra='forbid')
    type: str

filters.Begin = Begin
filters.End = End
filters.Uppercase = Uppercase
sys.modules['filters'] = filters

from validate_chunks import validate_chunks

@pytest.mark.parametrize("idx, val, msg", [
    (0, 1, "Invalid sub-list type at position 0"),
    (1, "x", "Invalid sub-list type at position 1"),
    (2, 1, "Invalid sub-list type at position 2"),
    (3, 1, "Invalid sub-list type at position 3"),
    (4, "x", "Invalid sub-list type at position 4"),
])
def test_invalid_types(idx, val, msg):
    data = ["a", {}, "c", "d", {}]
    data[idx] = val
    with pytest.raises(ValueError, match=msg):
        validate_chunks([data])

def test_invalid_length():
    with pytest.raises(ValueError, match="Invalid sub-list length"):
        validate_chunks([["a", {}, "c", "d"]])

def test_invalid_type_root():
    with pytest.raises(ValueError, match="Invalid type"):
        validate_chunks([123])

def test_valid_transformation():
    data = [
        "skip",
        ["a", {"type": "Begin", "source": "s", "shift": 1, "skip": 1, "add": 1}, "c", "d", {"type": "End"}],
        "keep"
    ]
    res = validate_chunks(data)
    assert res[0] == "skip"
    assert res[2] == "keep"
    sub = res[1]
    assert len(sub) == 7
    assert isinstance(sub[2], Begin)
    assert isinstance(sub[6], End)
    assert sub[1] == {"type": "Begin", "source": "s", "shift": 1, "skip": 1, "add": 1}
    assert sub[5] == {"type": "End"}

def test_extra_forbid():
    data = ["a", {"type": "Begin", "source": "s", "extra": 1}, "c", "d", {"type": "End"}]
    with pytest.raises(ValueError):
        validate_chunks([data])