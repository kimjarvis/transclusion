import pytest
from pathlib import Path
from src.transclude.types.include import Include


def test_include_basic(tmp_path):
    file_path = tmp_path / "content.txt"
    file_path.write_text("included content")

    inc = Include(type="Include", source=str(file_path))
    result = inc.execute("line1\nline2\n", {})

    assert result == "included content"


def test_include_head_tail(tmp_path):
    file_path = tmp_path / "content.txt"
    file_path.write_text("INSERTED")

    inc = Include(type="Include", source=str(file_path), head=1, tail=1)
    data = "head\nmiddle\ntail\n"
    result = inc.execute(data, {})

    assert result == "head\nINSERTEDtail\n"


def test_include_invalid_source(tmp_path):
    inc = Include(type="Include", source="nonexistent.txt")

    with pytest.raises(ValueError):
        inc.execute("data", {})


def test_include_head_tail_overflow(tmp_path):
    file_path = tmp_path / "content.txt"
    file_path.write_text("x")

    inc = Include(type="Include", source=str(file_path), head=5, tail=5)

    with pytest.raises(ValueError):
        inc.execute("line1\nline2\n", {})