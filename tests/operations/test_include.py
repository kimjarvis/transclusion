import pytest
from pathlib import Path
from src.transclude.operations.include import Include


@pytest.mark.parametrize("file,key,error", [
    (None, None, "Exactly one"),
    ("path.txt", "key", "Exactly one"),
])
def test_include_validation(file, key, error):
    with pytest.raises(ValueError, match=error):
        Include(type="Include", file=file, key=key)


def test_include_phase_one():
    op = Include(type="Include", file="dummy.txt", head=1, tail=1)
    data = "line1\nline2\nline3\n"
    result = op.phase_one(data, {})
    assert result == "line1\nline3\n"


def test_include_phase_two_file(tmp_path):
    file_path = tmp_path / "content.txt"
    file_path.write_text("INCLUDED", encoding='utf-8')
    op = Include(type="Include", file=str(file_path), head=1, tail=1)
    data = "pre\npost\n"
    result = op.phase_two(data, {})
    assert result == "pre\nINCLUDEDpost\n"


def test_include_phase_two_key():
    op = Include(type="Include", key="my_key", head=1, tail=1)
    data = "pre\npost\n"
    state = {"my_key": "INCLUDED"}
    result = op.phase_two(data, state)
    assert result == "pre\nINCLUDEDpost\n"


def test_include_phase_two_missing_file():
    op = Include(type="Include", file="nonexistent.txt")
    with pytest.raises(FileNotFoundError):
        op.phase_two("data", {})


def test_include_phase_two_missing_key():
    op = Include(type="Include", key="missing")
    with pytest.raises(KeyError):
        op.phase_two("data", {})