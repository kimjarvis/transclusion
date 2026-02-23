import pytest
from pathlib import Path
from src.transclude.operations.source import Source


def test_source_write_file(tmp_path):
    file_path = tmp_path / "output.txt"
    op = Source(type="Source", file=str(file_path))
    data = "line1\nline2\nline3\n"
    result = op.phase_one(data, {})

    assert result == data
    assert file_path.read_text() == data


def test_source_write_state():
    op = Source(type="Source", key="output")
    data = "line1\nline2\n"
    state = {}
    result = op.phase_one(data, state)

    assert result == data
    assert state["output"] == data


def test_source_head_tail(tmp_path):
    file_path = tmp_path / "trimmed.txt"
    op = Source(type="Source", file=str(file_path), head=1, tail=1)
    data = "line1\nline2\nline3\nline4\n"
    op.phase_one(data, {})

    assert file_path.read_text() == "line2\nline3\n"


def test_source_xor_violation():
    with pytest.raises(ValueError):
        Source(type="Source", file="path", key="key")

    with pytest.raises(ValueError):
        Source(type="Source")


def test_phase_two():
    op = Source(type="Source", key="test")
    assert op.phase_two("data", {}) == "data"


def test_source_validation_missing():
    with pytest.raises(ValueError):
        Source(type="Source", head=1)


def test_source_validation_both():
    with pytest.raises(ValueError):
        Source(type="Source", file="x", key="y")

def test_source_head_tail(tmp_path):
    file_path = tmp_path / "trimmed.txt"
    op = Source(type="Source", file=str(file_path), head=1, tail=1)
    data = "line1\nline2\nline3\nline4\n"
    op.phase_one(data, {})

    assert file_path.read_text() == "line2\nline3\n"

def test_source_validation_xor():
    with pytest.raises(ValueError):
        Source(type="Source", head=1)
    with pytest.raises(ValueError):
        Source(type="Source", file="x", key="y")

@pytest.mark.parametrize(
    "strip,lstrip,rstrip,data,expected",
    [
        (None, None, None, "  content  ", "  content  "),
        (" ", None, None, "  content  ", "content"),
        ("", None, None, "  content  ", "content"),
        (None, " ", None, "  content  ", "content  "),
        (None, "", None, "  content  ", "content  "),
        (None, None, " ", "  content  ", "  content"),
        (None, None, "", "  content  ", "  content"),
        (" ", "c", "t", "  content  ", "onten"),
    ]
)
def test_source_strip_variations(strip, lstrip, rstrip, data, expected):
    op = Source(type="Source", key="out", strip=strip, lstrip=lstrip, rstrip=rstrip)
    state = {}
    op.phase_one(data, state)
    assert state["out"] == expected


def test_source_strip_chars():
    op = Source(type="Source", key="res", strip="x")
    state = {}
    op.phase_one("xdatax", state)
    assert state["res"] == "data"