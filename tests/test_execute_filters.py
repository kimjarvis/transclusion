import pytest
from src.transclude.execute_filters import execute_filters
from src.transclude.operation import Operation


class MockTransclude(Operation):
    type: str = "Mock"
    mock_return: str = ""

    def execute(self, data: str, state: dict) -> str:
        return self.mock_return


def test_valid_execution_changed():
    mock_obj = MockTransclude(mock_return="modified")
    input_data = [["a", {}, mock_obj, "original", "e", "f"]]
    output = execute_filters(input_data, {})
    assert output[0][6] == "modified"
    assert output[0][7] is True


def test_valid_execution_unchanged():
    mock_obj = MockTransclude(mock_return="original")
    input_data = [["a", {}, mock_obj, "original", "e", "f"]]
    output = execute_filters(input_data, {})
    assert output[0][6] == "original"
    assert output[0][7] is False


def test_invalid_sublist_length():
    with pytest.raises(ValueError):
        execute_filters([["a", "b"]], {})


def test_invalid_object_type():
    with pytest.raises(ValueError):
        execute_filters([["a", {}, "not_an_obj", "str", "e", "f"]], {})


def test_invalid_string_type():
    mock_obj = MockTransclude()
    with pytest.raises(ValueError):
        execute_filters([["a", {}, mock_obj, 123, "e", "f"]], {})


def test_non_list_items_preserved():
    input_data = ["string", ["a", {}, MockTransclude(), "s", "e", "f"], 123]
    output = execute_filters(input_data, {})
    assert output[0] == "string"
    assert output[2] == 123