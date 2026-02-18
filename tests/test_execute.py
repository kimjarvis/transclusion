import pytest
from execute import execute, Base

class MockBase(Base):
    def execute(self, data: str) -> str:
        return data

class MockChangeBase(Base):
    def execute(self, data: str) -> str:
        return f"changed_{data}"

def test_valid_no_change():
    data = [["a", {}, MockBase(), "str", "x", {}, None]]
    result = execute(data)
    assert result[0][7] == "str"
    assert result[0][8] is False

def test_valid_change():
    data = [["a", {}, MockChangeBase(), "str", "x", {}, None]]
    result = execute(data)
    assert result[0][7] == "changed_str"
    assert result[0][8] is True

def test_invalid_sublist_length():
    data = [["a", {}, MockBase()]]
    with pytest.raises(ValueError):
        execute(data)

def test_invalid_base_type():
    data = [["a", {}, "not_base", "str", "x", {}, None]]
    with pytest.raises(TypeError):
        execute(data)

def test_invalid_string_type():
    data = [["a", {}, MockBase(), 123, "x", {}, None]]
    with pytest.raises(TypeError):
        execute(data)

def test_non_list_items_ignored():
    data = ["string", {"dict": 1}, ["a", {}, MockBase(), "str", "x", {}, None]]
    result = execute(data)
    assert result[0] == "string"
    assert result[1] == {"dict": 1}
    assert len(result[2]) == 9

def test_invalid_dict_structure_surrounding():
    # Ensures function handles dicts at indices 1 and 5 without error
    data = [["a", {"k": "v"}, MockBase(), "str", "x", {"k": "v"}, None]]
    result = execute(data)
    assert result[0][1] == {"k": "v"}
    assert result[0][5] == {"k": "v"}