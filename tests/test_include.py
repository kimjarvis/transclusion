import pytest
from pathlib import Path
from _include import Include

def test_execute_valid_file(tmp_path):
    file = tmp_path / "test.txt"
    file.write_text("content", encoding="utf-8")
    inc = Include(type="test", file=str(file))
    assert inc.execute("", {}) == "content"

def test_execute_valid_symlink(tmp_path):
    target = tmp_path / "target.txt"
    target.write_text("linked", encoding="utf-8")
    link = tmp_path / "link.txt"
    link.symlink_to(target)
    inc = Include(type="test", file=str(link))
    assert inc.execute("", {}) == "linked"

def test_execute_missing_file():
    inc = Include(type="test", file="/nonexistent/path.txt")
    with pytest.raises(FileNotFoundError):
        inc.execute("", {})

def test_execute_directory(tmp_path):
    inc = Include(type="test", file=str(tmp_path))
    with pytest.raises(FileNotFoundError):
        inc.execute("", {})