import os
import tempfile
from src.transclude.operations.source import Source


def test_source_head():
    src = Source(type="Source", key="test", head=1)
    data = "line1\nline2\nline3"
    state = {}
    result = src.phase_one(data, state)
    assert result == "line2\nline3"
    assert state["test"] == "line2\nline3"


def test_source_tail():
    src = Source(type="Source", key="test", tail=1)
    data = "line1\nline2\nline3"
    state = {}
    result = src.phase_one(data, state)
    assert result == "line1\nline2"


def test_source_file_write():
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as tmp:
        path = tmp.name

    try:
        src = Source(type="Source", file=path)
        data = "content"
        state = {}
        src.phase_one(data, state)

        with open(path, 'r', encoding='utf-8') as f:
            assert f.read() == "content"
    finally:
        os.unlink(path)


def test_source_validation_missing():
    try:
        Source(type="Source")
        assert False, "Should raise ValueError"
    except ValueError:
        pass


def test_source_validation_both():
    try:
        Source(type="Source", file="x", key="y")
        assert False, "Should raise ValueError"
    except ValueError:
        pass


def test_source_phase_two():
    src = Source(type="Source", key="test")
    assert src.phase_two("data", {}) == "data"