import pytest
from validate_chunks import ChunkValidator
from pydantic import BaseModel

class DummyModel(BaseModel):
    type: str

@pytest.fixture
def validator():
    v = ChunkValidator()
    v.register("dummy", DummyModel)
    return v

def test_invalid_top_level_type(validator):
    with pytest.raises(ValueError, match="Invalid type"):
        validator.validate_chunks([123])

def test_invalid_sub_list_length(validator):
    with pytest.raises(ValueError, match="Invalid sub-list length"):
        validator.validate_chunks([["a", {}, "c", "d"]])

@pytest.mark.parametrize("idx, val, msg", [
    (0, 1, "Invalid sub-list type at position 0"),
    (1, "x", "Invalid sub-list type at position 1"),
    (2, 1, "Invalid sub-list type at position 2"),
    (3, 1, "Invalid sub-list type at position 3"),
    (4, "x", "Invalid sub-list type at position 4"),
])
def test_invalid_types(validator, idx, val, msg):
    data = ["a", {"type": "dummy"}, "c", "d", {"type": "dummy"}]
    data[idx] = val
    with pytest.raises(ValueError, match=msg):
        validator.validate_chunks([data])

def test_missing_type_key(validator):
    data = ["a", {}, "c", "d", {"type": "dummy"}]
    with pytest.raises(ValueError, match="Missing type key"):
        validator.validate_chunks([data])

def test_unknown_registry_type(validator):
    data = ["a", {"type": "unknown"}, "c", "d", {"type": "dummy"}]
    with pytest.raises(ValueError, match="Unknown type"):
        validator.validate_chunks([data])

def test_valid_transformation(validator):
    data = ["m", {"type": "dummy"}, "c", "d", {"type": "dummy"}]
    result = validator.validate_chunks([data])
    assert len(result) == 1
    sub = result[0]
    assert len(sub) == 7
    assert isinstance(sub[2], DummyModel)
    assert isinstance(sub[6], DummyModel)