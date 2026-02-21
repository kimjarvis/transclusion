import pytest
from pathlib import Path
from src.transclude.operations.include import Include


def test_phase_one_head_tail_zero():
    inc = Include(type="Include", source="dummy.txt")
    assert inc.phase_one("line1\nline2\n", {}) == ""


def test_phase_one_head_tail_split():
    inc = Include(type="Include", source="dummy.txt", head=1, tail=1)
    assert inc.phase_one("line1\nline2\nline3\nline4\n", {}) == "line1\nline4\n"


def test_phase_one_head_tail_overlap_error():
    inc = Include(type="Include", source="dummy.txt", head=3, tail=3)
    with pytest.raises(ValueError):
        inc.phase_one("line1\nline2\n", {})


def test_phase_two_file_insertion(tmp_path):
    file_path = tmp_path / "content.txt"
    file_path.write_text("xxx", encoding="utf-8")

    inc = Include(type="Include", source=str(file_path), head=1, tail=1)
    data = "line1\nline2\nline3\nline4\n"
    assert inc.phase_two(data, {}) == "line1\nxxxline4\n"


def test_phase_two_invalid_source():
    inc = Include(type="Include", source="/nonexistent/path", head=0, tail=0)
    with pytest.raises(ValueError):
        inc.phase_two("data", {})