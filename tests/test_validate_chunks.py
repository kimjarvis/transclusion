import pytest
from pydantic import ValidationError
from validate_chunks import validate_chunks, Begin, End


def test_valid_chunks():
    data = [["A", {"type": "Begin", "source": "s", "shift": 1}, "B", "C", {"type": "End"}]]
    result = validate_chunks(data)
    assert len(result[0]) == 7
    assert isinstance(result[0][2], Begin)
    assert isinstance(result[0][6], End)


def test_invalid_length():
    with pytest.raises(ValueError, match="Invalid sub-list length"):
        validate_chunks([["a", {}, "c", "d"]])


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


def test_invalid_type_parameter():
    with pytest.raises(ValueError, match="Invalid parameter: type"):
        validate_chunks([["a", {"type": "Unknown"}, "c", "d", {"type": "End"}]])


def test_pydantic_validation_error():
    with pytest.raises(ValidationError):
        validate_chunks([["a", {"type": "Begin"}, "c", "d", {"type": "End"}]])
    with pytest.raises(ValidationError):
        validate_chunks([["a", {"type": "Begin", "source": "s", "extra": 1}, "c", "d", {"type": "End"}]])