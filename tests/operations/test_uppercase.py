from src.transclude.operations.uppercase import Uppercase

def test_instantiation():
    u = Uppercase()
    assert u.type == "Uppercase"

def test_execute_lowercase():
    u = Uppercase()
    assert u.execute("hello", {}) == "HELLO"

def test_execute_mixed_case():
    u = Uppercase()
    assert u.execute("Hello World", {}) == "HELLO WORLD"