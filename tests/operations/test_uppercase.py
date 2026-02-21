from src.transclude.operations.uppercase import Uppercase

def test_instantiation():
    op = Uppercase()
    assert op.type == "Uppercase"

def test_phase_one_pass_through():
    op = Uppercase()
    assert op.phase_one("Hello", {}) == "Hello"

def test_phase_two_uppercase():
    op = Uppercase()
    assert op.phase_two("Hello", {}) == "HELLO"