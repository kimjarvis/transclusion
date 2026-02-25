import pytest
from pathlib import Path
from src.syncspec.directives.source import Source

@pytest.mark.parametrize("file,key,valid", [
    ("path.txt", None, True),
    (None, "my_key", True),
    ("path.txt", "my_key", False),
    (None, None, False),
])
def test_source_validation(file, key, valid):
    if valid:
        Source(syncspec="Source", file=file, key=key)
    else:
        with pytest.raises(ValueError):
            Source(syncspec="Source", file=file, key=key)

def test_source_defaults():
    s = Source(syncspec="Source", key="k")
    assert s.head == 1
    assert s.tail == 1

def test_phase_one_file(tmp_path):
    file_path = tmp_path / "out.txt"
    s = Source(syncspec="Source", file=str(file_path), head=1, tail=1)
    data = "line1\nline2\nline3\n"
    res = s.phase_one(data, {})
    assert res == data
    assert file_path.read_text() == "line2\n"

def test_phase_one_state():
    s = Source(syncspec="Source", key="k", head=1, tail=1)
    data = "line1\nline2\nline3\n"
    state = {}
    res = s.phase_one(data, state)
    assert res == data
    assert state["k"] == "line2\n"

def test_phase_two():
    s = Source(syncspec="Source", key="k")
    data = "content"
    assert s.phase_two(data, {}) == data