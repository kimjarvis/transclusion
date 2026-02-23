import pytest
from src.transclude.operations.source import Source

@pytest.mark.parametrize("file,key,expected_error", [
    ("out.txt", None, None),
    (None, "my_key", None),
    (None, None, "Exactly one of 'file' or 'key' must be specified"),
    ("out.txt", "my_key", "Exactly one of 'file' or 'key' must be specified"),
])
def test_source_validation(file, key, expected_error):
    if expected_error:
        with pytest.raises(ValueError, match=expected_error):
            Source(type="Source", file=file, key=key)
    else:
        src = Source(type="Source", file=file, key=key)
        assert src.type == "Source"

def test_phase_one_file(tmp_path):
    file_path = tmp_path / "out.txt"
    src = Source(type="Source", file=str(file_path), head=1, tail=1, front=1, bask=1)
    data = "line1\nline2\nline3\n"
    state = {}
    # Mock split behavior implicitly via logic verification if split is external
    # Assuming split returns middle section based on args
    result = src.phase_one(data, state)
    assert result == data
    assert file_path.read_text() == "ine2" # Depends on split implementation logic

def test_phase_one_key():
    src = Source(type="Source", key="content")
    data = "test"
    state = {}
    result = src.phase_one(data, state)
    assert result == data
    assert state["content"] == "test" # Depends on split returning full string if args 0

def test_phase_two():
    src = Source(type="Source", key="k")
    assert src.phase_two("data", {}) == "data"