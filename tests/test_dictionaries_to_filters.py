import pytest
from pydantic import BaseModel
from dictionaries_to_filters import Registry

class DummyModel(BaseModel):
    type: str

@pytest.fixture
def validator():
    v = Registry()
    v.register("dummy", DummyModel)
    return v

def test_invalid_top_level_type(validator):
    with pytest.raises(ValueError, match="Invalid type"):
        validator.dictionaries_to_filters([123])

def test_invalid_sublist_length(validator):
    with pytest.raises(ValueError, match="Invalid sub-list length"):
        validator.dictionaries_to_filters([["a", {}, "c", "d"]])

@pytest.mark.parametrize("idx, val, msg", [
    (0, 1, "Invalid sub-list type at position 0"),
    (1, "x", "Invalid sub-list type at position 1"),
    (2, 1, "Invalid sub-list type at position 2"),
    (3, 1, "Invalid sub-list type at position 3"),
    (4, "x", "Invalid sub-list type at position 4"),
])
def test_invalid_types(validator, idx, val, msg):
    data = ["a", {}, "c", "d", {}]
    data[idx] = val
    with pytest.raises(ValueError, match=msg):
        validator.dictionaries_to_filters([data])

def test_conflicting_keys(validator):
    data = ["a", {"key": 1}, "c", "d", {"key": 2}]
    with pytest.raises(ValueError, match="Conflicting keys found"):
        validator.dictionaries_to_filters([data])

def test_missing_type_key(validator):
    data = ["a", {}, "c", "d", {}]
    with pytest.raises(ValueError, match="Missing 'type' key"):
        validator.dictionaries_to_filters([data])

def test_unknown_type(validator):
    data = ["a", {"type": "unknown"}, "c", "d", {}]
    with pytest.raises(ValueError, match="Unknown type"):
        validator.dictionaries_to_filters([data])

def test_valid_flow(validator):
    data = ["a", {"type": "dummy"}, "c", "d", {}]
    result = validator.dictionaries_to_filters([data])
    assert len(result) == 1
    assert len(result[0]) == 6
    assert isinstance(result[0][2], DummyModel)