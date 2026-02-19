import pytest
from reassemble_document import reassemble_document

@pytest.mark.parametrize("input_data,expected", [
    (["m", ["a", "b", "c", "d", "e", "g", "h", True], "n"], (True, "m{{a}}h{{e}}n")),
    (["x", ["1", "2", "3", "4", "5", "6", "7", False]], (False, "x{{1}}7{{5}}")),
])
def test_reassemble_document_success(input_data, expected):
    assert reassemble_document(input_data) == expected

@pytest.mark.parametrize("input_data,error_msg", [
    (["a", ["short"]], "Inner list length must be exactly 8"),
    (["a", [1, "b", "c", "d", "e", "g", "h", True]], "Item at index 0 must be a string"),
    (["a", ["a", "b", "c", "d", "e", "g", 6, True]], "Item at index 6 must be a string"),
    (["a", ["a", "b", "c", "d", 4, "g", "h", True]], "Item at index 4 must be a string"),
    (["a", ["a", "b", "c", "d", "e", "g", "h", "True"]], "Item at index 7 must be a boolean"),
    (["a", 123], "Top-level items must be string or list"),
])
def test_reassemble_document_errors(input_data, error_msg):
    with pytest.raises(ValueError, match=error_msg):
        reassemble_document(input_data)