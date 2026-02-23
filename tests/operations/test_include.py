import pytest
from src.transclude.operations.include import Include

def test_include_validation_mutual_exclusion():
    with pytest.raises(ValueError):
        Include(type="Include", head=1)
    with pytest.raises(ValueError):
        Include(type="Include", file="a.txt", key="b")

def test_include_phase_one_trim():
    op = Include(type="Include", file="dummy", head=1, tail=1)
    data = "line1\nline2\nline3\nline4\n"
    assert op.phase_one(data, {}) == "line1\nline4\n"

def test_include_phase_one_empty():
    op = Include(type="Include", file="dummy", head=0, tail=0)
    data = "line1\nline2\nline3\nline4\n"
    assert op.phase_one(data, {}) == ""

def test_include_phase_one_error():
    op = Include(type="Include", file="dummy", head=3, tail=3)
    data = "line1\nline2\n"
    with pytest.raises(ValueError):
        op.phase_one(data, {})

def test_include_phase_two_file_injection(tmp_path):
    file = tmp_path / "test.txt"
    file.write_text("xxx")
    op = Include(type="Include", file=str(file), head=1, tail=1)
    data = "line1\nline2\nline3\nline4\n"
    assert op.phase_two(data, {}) == "line1\nxxxline4\n"

def test_include_phase_two_key_injection():
    op = Include(type="Include", key="content", head=0, tail=0)
    data = "line1\nline2\n"
    assert op.phase_two(data, {"content": "yyy"}) == "yyy"

def test_include_phase_two_missing_key():
    op = Include(type="Include", key="missing", head=0, tail=0)
    with pytest.raises(ValueError):
        op.phase_two("data", {})

def test_include_phase_two_missing_file():
    op = Include(type="Include", file="/nonexistent", head=0, tail=0)
    with pytest.raises(ValueError):
        op.phase_two("data", {})

def test_phase_two_prefix_suffix():
    import tempfile
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
        f.write("xxx")
        path = f.name
    try:
        op = Include(type="Include", file=path, head=0, tail=0, prefix="[", suffix="]")
        data = "line1\n"
        assert op.phase_two(data, {}) == "[xxx]"
    finally:
        import os
        os.unlink(path)