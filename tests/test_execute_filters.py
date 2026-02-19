import pytest
from abc import ABC, abstractmethod
from unittest.mock import MagicMock
import sys

from src.transclusion.execute_filters import Base

class MockBegin(Base):
    def execute(self, data: str, state: dict) -> str:
        return data

class MockChangedBegin(Base):
    def execute(self, data: str, state: dict) -> str:
        return f"changed_{data}"

# Patch filters module before importing solution
sys.modules['filters'] = MagicMock()
sys.modules['filters'].Base = Base

from src.transclusion.execute_filters import execute_filters

def test_valid_no_change():
    state = {}
    item = ['A', {}, MockBegin(), 'B', 'C', {}]
    result = execute_filters([item], state)
    assert result[0][6] == 'B'
    assert result[0][7] is False

def test_valid_changed():
    state = {}
    item = ['A', {}, MockChangedBegin(), 'B', 'C', {}]
    result = execute_filters([item], state)
    assert result[0][6] == 'changed_B'
    assert result[0][7] is True

def test_invalid_sublist_length():
    with pytest.raises(ValueError):
        execute_filters([['A', {}, MockBegin(), 'B']], {})

def test_invalid_base_type():
    with pytest.raises(TypeError):
        execute_filters([['A', {}, "NotBase", 'B', 'C', {}]], {})

def test_invalid_string_type():
    with pytest.raises(TypeError):
        execute_filters([['A', {}, MockBegin(), 123, 'C', {}]], {})

def test_non_list_items():
    result = execute_filters(['string', 123], {})
    assert result == ['string', 123]