import pytest
from src.syncspec.execute_phase_one import execute_phase_one
from src.syncspec.directive import Directive

class MockDirective(Directive):
    type: str = "Mock"
    def phase_one(self, data: str, state: dict) -> str:
        return f"processed:{data}"
    def phase_two(self, data: str, state: dict) -> str:
        return ""

def test_valid_execution():
    state = {"key": "value"}
    op = MockDirective()
    data = [["A", {}, op, "input", "C", {}]]
    result = execute_phase_one(data, state)
    assert result[0][-1] == "processed:input"
    assert len(result[0]) == 7

def test_invalid_directive_type():
    state = {}
    data = [["A", {}, "not_an_op", "input", "C", {}]]
    with pytest.raises(ValueError, match="must be an Directive instance"):
        execute_phase_one(data, state)

def test_invalid_data_type():
    state = {}
    op = MockDirective()
    data = [["A", {}, op, 123, "C", {}]]
    with pytest.raises(ValueError, match="must be a string"):
        execute_phase_one(data, state)

def test_sublist_too_short():
    state = {}
    data = [["A", {}, "op"]]
    with pytest.raises(ValueError, match="must have at least 6 elements"):
        execute_phase_one(data, state)

def test_non_list_items_ignored():
    state = {}
    op = MockDirective()
    data = ["string", {"dict": True}, ["A", {}, op, "input", "C", {}]]
    result = execute_phase_one(data, state)
    assert len(result) == 3
    assert len(result[2]) == 7