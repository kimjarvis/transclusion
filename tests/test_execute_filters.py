import pytest
from typing import Any
from abc import ABC, abstractmethod
from unittest.mock import patch, MagicMock
import sys

# Mock Base class for testing if filters module is unavailable
class Base(ABC):
    @abstractmethod
    def execute(self, data: str) -> str:
        pass

class MockBegin(Base):
    def execute(self, data: str) -> str:
        return data

class MockChangedBegin(Base):
    def execute(self, data: str) -> str:
        return f"changed_{data}"

# Patch filters.Base before importing solution
sys.modules['filters'] = MagicMock()
sys.modules['filters'].Base = Base

from execute_filters import execute_filters

def test_valid_input_no_change():
    obj = MockBegin()
    data = ['A', {}, obj, 'B', 'C', {}]
    result = execute_filters([data])
    assert result[0][6] == 'B'
    assert result[0][7] is False

def test_valid_input_changed():
    obj = MockChangedBegin()
    data = ['A', {}, obj, 'B', 'C', {}]
    result = execute_filters([data])
    assert result[0][6] == 'changed_B'
    assert result[0][7] is True

def test_invalid_sublist_length():
    with pytest.raises(ValueError):
        execute_filters([['A', 'B']])

def test_invalid_base_type():
    with pytest.raises(TypeError):
        execute_filters([['A', {}, 'NotBase', 'B', 'C', {}]])

def test_invalid_string_type():
    class ValidBase(Base):
        def execute(self, data: str) -> str: return data
    with pytest.raises(TypeError):
        execute_filters([['A', {}, ValidBase(), 123, 'C', {}]])

def test_non_list_items_ignored():
    result = execute_filters(['string', 123, None])
    assert result == ['string', 123, None]