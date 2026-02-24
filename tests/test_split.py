import pytest
from src.transclude.split import split, TextSplit

@pytest.mark.parametrize("text, head, tail, expected", [
    ("line1\nline2\nline3\n", 1, 1, ("line1\n", "line2\n", "line3\n")),
    ("line1\nline2\nline3", 1, 1, ("line1\n", "line2\n", "line3")),
    ("line1\nline3\n", 1, 1, ("line1\n", "", "line3\n")),
    ("a\nb\n", 0, 0, ("", "a\nb\n", "")),
    ("a\nb\n", 1, 0, ("a\n", "b\n", "")),
    ("line\n", 0, 0, ("", "line\n", "")),
    ("ab\ncd", 1, 1, ("ab\n", "", "cd")),
    ("abcd", 1, 0, ("abcd", "", "")),
    ("abcd", 0, 0, ("", "abcd", "")),
    ("ab\ncd", 1, 0, ("ab\n", "cd", "")),
    ("ab\ncd\n", 1, 1, ("ab\n", "", "cd\n")),
    ("ab\ncd\n", 2, 0, ("ab\ncd\n", "", "")),
    ("", 0, 0, ("", "", "")),
])
def test_split_valid(text, head, tail, expected):
    result = split(text, head, tail)
    assert result == TextSplit(*expected)
    assert result.top + result.middle + result.bottom == text

@pytest.mark.parametrize("text, head, tail", [
    ("abcd\n", 1, 1),
    ("ab\ncd\n", 2, 1),
    ("", 1, 1),
])
def test_split_errors(text, head, tail):
    with pytest.raises(ValueError):
        split(text, head, tail)

def test_split_negative():
    with pytest.raises(ValueError):
        split("text", -1, 0)