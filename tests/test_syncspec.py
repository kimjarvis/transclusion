import os
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock
from src.syncspec.syncspec import Syncspec


@pytest.fixture
def syncspec():
    return Syncspec()


@pytest.fixture
def temp_dir(tmp_path):
    return tmp_path


@pytest.mark.parametrize("content,expected", [
    ("hello", "processed_hello"),
    ("{{var}}", "processed_{{var}}"),
])
def test_render_file_transforms_content(syncspec, temp_dir, content, expected):
    file_path = temp_dir / "test.txt"
    file_path.write_text(content, encoding='utf-8')

    with patch.object(syncspec, 'render_string', return_value=(True, f"processed_{content}")):
        syncspec.render_file(str(file_path))

    assert file_path.read_text(encoding='utf-8') == expected


def test_render_file_ignores_binary(syncspec, temp_dir):
    file_path = temp_dir / "binary.bin"
    file_path.write_bytes(b'\x00\x01\x02')

    # Should not raise
    syncspec.render_file(str(file_path))


def test_render_file_raises_on_missing(syncspec):
    with pytest.raises(FileNotFoundError):
        syncspec.render_file("/nonexistent/file.txt")


@pytest.mark.parametrize("files,patterns,processed_count", [
    (["a.txt", "b.log"], None, 2),
    (["a.txt", "b.log"], ["*.log"], 1),
    (["a.txt", "sub/c.txt"], ["sub/*"], 1),
])
def test_render_directory_filters_files(syncspec, temp_dir, files, patterns, processed_count):
    for f in files:
        path = temp_dir / f
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("data", encoding='utf-8')

    with patch.object(syncspec, 'render_file', wraps=syncspec.render_file) as mock_render:
        syncspec.render_directory(str(temp_dir), patterns)
        assert mock_render.call_count == processed_count


def test_render_paths_iterates_directories(syncspec, temp_dir):
    dir1 = temp_dir / "d1"
    dir2 = temp_dir / "d2"
    dir1.mkdir()
    dir2.mkdir()
    (dir1 / "f.txt").write_text("1", encoding='utf-8')
    (dir2 / "f.txt").write_text("2", encoding='utf-8')

    with patch.object(syncspec, 'render_file') as mock_render:
        syncspec.render_paths([str(dir1), str(dir2)])
        assert mock_render.call_count == 2