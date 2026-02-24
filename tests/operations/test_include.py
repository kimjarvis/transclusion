import pytest
from pathlib import Path
from src.transclude.operations.include import Include


@pytest.mark.parametrize("file,key", [(None, None), ("path.txt", "key")])
def test_include_validation_errors(file, key):
    with pytest.raises(ValueError):
        Include(type="Include", file=file, key=key)


def test_include_phase_one(tmp_path):
    data = "line1\nline2\nline3\nline4\n"
    inc = Include(type="Include", key="k", head=1, tail=1)
    # split removes 1 head, 1 tail -> middle="line2\nline3\n", top="line1\n", bottom="line4\n"
    # phase_one returns top + bottom
    result = inc.phase_one(data, {})
    assert result == "line1\nline4\n"


def test_include_phase_two_file(tmp_path):
    file_path = tmp_path / "content.txt"
    file_path.write_text("INSERTED", encoding='utf-8')
    data = "line1\nline2\nline3\nline4\n"

    inc = Include(type="Include", file=str(file_path), head=1, tail=1)
    result = inc.phase_two(data, {})
    assert result == "line1\nINSERTEDline4\n"


def test_include_phase_two_key():
    data = "line1\nline2\nline3\nline4\n"
    state = {"my_key": "VALUE"}
    inc = Include(type="Include", key="my_key", head=1, tail=1)
    result = inc.phase_two(data, state)
    assert result == "line1\nVALUEline4\n"


def test_include_phase_two_file_not_found():
    inc = Include(type="Include", file="/nonexistent.txt")
    with pytest.raises(FileNotFoundError):
        inc.phase_two("data", {})


def test_include_phase_two_key_missing():
    inc = Include(type="Include", key="missing_key")
    with pytest.raises(KeyError):
        inc.phase_two("data", {})