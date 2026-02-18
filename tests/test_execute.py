import pytest
from execute import execute, Base

class MockBase(Base):
    def __init__(self, return_val):
        self.return_val = return_val
    def execute(self, data: str) -> str:
        return self.return_val

def get_valid_sublist(change=False):
    val = "new" if change else "B"
    return ["A", {}, MockBase(val), "B", "C", {}, MockBase("")]

def test_execute_valid_no_change():
    data = [get_valid_sublist(change=False)]
    res = execute(data)
    assert res[0][-2] == "B"
    assert res[0][-1] is False

def test_execute_valid_change():
    data = [get_valid_sublist(change=True)]
    res = execute(data)
    assert res[0][-2] == "new"
    assert res[0][-1] is True

def test_execute_invalid_length():
    with pytest.raises(ValueError):
        execute([["A", {}, MockBase(""), "B"]])

def test_execute_invalid_type():
    # Position 2 should be Base, passing str
    with pytest.raises(ValueError):
        execute([["A", {}, "NotBase", "B", "C", {}, MockBase("")]])

def test_execute_invalid_dict_structure():
    # Position 1 should be dict, passing list
    with pytest.raises(ValueError):
        execute([["A", [], MockBase(""), "B", "C", {}, MockBase("")]])

def test_execute_mixed_outer_list():
    data = ["str", get_valid_sublist(), "str"]
    res = execute(data)
    assert res[0] == "str"
    assert len(res[1]) == 9
    assert res[2] == "str"