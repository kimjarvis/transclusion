import pytest
from src.syncspec.reassemble_document import reassemble_document

@pytest.mark.parametrize("data, expected", [
    (["m", ["a","b","c","d","e","g","h","i",True], "n"], (True, "m{{a}}i{{e}}n")),
    (["x", ["1","2","3","4","5","6","7","8",False], "y"], (False, "x{{1}}8{{5}}y")),
])
def test_valid_reassembly(data, expected):
    assert reassemble_document(data) == expected

@pytest.mark.parametrize("data, msg", [
    (["a", ["short"], "b"], "List length must be 9"),
    (["a", [1]*9, "b"], "Index 0 must be string"),
    (["a", ["a","b","c","d","e","g","h",1,True], "b"], "Index 7 must be string"),
    (["a", ["a","b","c","d",1,"g","h","i",True], "b"], "Index 4 must be string"),
    (["a", ["a","b","c","d","e","g","h","i","1"], "b"], "Index 8 must be bool"),
    (["a", 123, "b"], "Invalid item type"),
])
def test_invalid_inputs(data, msg):
    with pytest.raises(ValueError, match=msg):
        reassemble_document(data)