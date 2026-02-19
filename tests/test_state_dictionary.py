import pytest
from src.transclude.state_dictionary import State_dictionary

def test_init():
    assert State_dictionary().state == {}

def test_set_valid():
    s = State_dictionary()
    s.state['k'] = 'v'
    assert s.state['k'] == 'v'

def test_set_invalid():
    s = State_dictionary()
    with pytest.raises(ValueError):
        s.state['k'] = lambda x: x

def test_setdefault_invalid():
    s = State_dictionary()
    with pytest.raises(ValueError):
        s.state.setdefault('k', lambda x: x)

def test_update_invalid():
    s = State_dictionary()
    with pytest.raises(ValueError):
        s.state.update({'k': lambda x: x})

def test_dumps():
    s = State_dictionary()
    s.state['k'] = 'v'
    assert s.dumps() == '{"k": "v"}'

def test_loads():
    s = State_dictionary()
    s.loads('{"k": "v"}')
    assert s.state['k'] == 'v'