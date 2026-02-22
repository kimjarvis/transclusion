import pytest
from typing import Any
from src.transclude.operation import Operation
from src.transclude.execute_phase_two import execute_phase_two

class MockOp(Operation):
    type: str = "Mock"
    def phase_one(self, data: str, state: dict) -> str: return data
    def phase_two(self, data: str, state: dict) -> str:
        return state.get('prefix', '') + data

def test_valid_processing_changed():
    state = {'prefix': 'NEW_'}
    data = [['A', {}, MockOp(type='Mock'), 'B', 'C', {}, 'input']]
    result = execute_phase_two(data, state)
    assert result[0][7] == 'NEW_input'
    assert result[0][8] is True

# def test_valid_processing_unchanged():
#     state = {'prefix': ''}
#     data = [['A', {}, MockOp(type='Mock'), 'B', 'C', {}, 'input']]
#     result = execute_phase_two(data, state)
#     assert result[0][7] == 'input'
#     assert result[0][8] is False

def test_invalid_sublist_length():
    with pytest.raises(ValueError):
        execute_phase_two([['short', 'list']], {})

def test_invalid_operation_type():
    with pytest.raises(ValueError):
        execute_phase_two([['A', {}, "NotAnOp", 'B', 'C', {}, 'input']], {})

def test_invalid_string_type():
    with pytest.raises(ValueError):
        execute_phase_two([['A', {}, MockOp(type='Mock'), 'B', 'C', {}, 123]], {})

def test_non_list_items_ignored():
    data = ['string', 1, ['A', {}, MockOp(type='Mock'), 'B', 'C', {}, 'input']]
    result = execute_phase_two(data, {})
    assert len(result) == 3
    assert len(result[2]) == 9