# test_split.py
import pytest
from src.transclude.split import split, TextSplit


# ======================
# HAPPY PATH TESTS
# ======================

@pytest.mark.parametrize("text,head,front,back,tail,expected", [
    # Example 1: Basic split with head/front/tail/back
    (
            "line1\nline2\nline3\n",
            1, 1, 1, 1,
            TextSplit("line1\nl", "ine2", "\nline3\n")
    ),

    # Example 2: Empty first/last with full middle
    (
            "a\nb\n",
            0, 0, 0, 0,
            TextSplit("", "a\nb\n", "")
    ),

    # Example 3: Line-based split
    (
            "a\nb\n",
            1, 0, 0, 1,
            TextSplit("a\n", "", "b\n")
    ),

    # Character-level split within single line
    (
            "hello",
            0, 2, 2, 0,
            TextSplit("he", "l", "lo")
    ),

    # Head-only split (no front/back)
    (
            "hello\nworld",
            1, 0, 0, 0,
            TextSplit("hello\n", "world", "")
    ),

    # Tail-only split (no front/back)
    (
            "hello\nworld",
            0, 0, 0, 1,
            TextSplit("", "hello\n", "world")
    ),

    # Tail split with newline preservation
    (
            "hello\nworld\n",
            0, 0, 0, 1,
            TextSplit("", "hello\n", "world\n")
    ),

    # Multi-line front/back with newline handling
    (
            "ab\ncd\nef\n",
            1, 2, 1, 1,
            TextSplit("ab\ncd", "", "\nef\n")
    ),
])
def test_split_happy_path(text, head, front, back, tail, expected):
    result = split(text, head, front, back, tail)
    assert result == expected
    assert result.first + result.middle + result.last == text


# ======================
# ERROR TESTS
# ======================

@pytest.mark.parametrize("text,head,front,back,tail,exc_msg", [
    # Negative parameter tests
    ("", -1, 0, 0, 0, "Negative values"),
    ("", 0, -1, 0, 0, "Negative values"),
    ("", 0, 0, -1, 0, "Negative values"),
    ("", 0, 0, 0, -1, "Negative values"),

    # Head > line count
    ("a", 2, 0, 0, 0, "Not enough lines for head part: text has 1 lines, but head=2"),

    # Tail > line count
    ("a", 0, 0, 0, 2, "Not enough lines for tail part: text has 1 lines, but tail=2"),

    # Head + front requires more lines
    ("a", 1, 1, 0, 0,
     "Not enough lines for front part: text has 1 lines, but head=1 and front>0 requires at least 2 lines"),

    # Tail + back requires more lines
    ("a", 0, 0, 1, 1,
     "Not enough lines for back part: text has 1 lines, but tail=1 and back>0 requires at least 2 lines"),

    # Insufficient first line characters (head=0)
    ("a", 0, 2, 0, 0,
     "Not enough characters in the first line for front part: first line has 1 characters, but front=2"),

    # Insufficient line characters for front (head>0)
    ("a\nb", 1, 2, 0, 0, "Not enough characters in line 1 for front part: line has 1 characters, but front=2"),

    # Insufficient last line characters (tail=0)
    ("a", 0, 0, 2, 0, "Not enough characters in the last line for back part: last line has 1 characters, but back=2"),

    # Insufficient line characters for back (tail>0)
    ("a\nb", 0, 0, 3, 1, "Not enough characters in line 0 for back part: line has 2 characters, but back=3"),

    # Front part contains newline
    ("ab\ncd\n", 1, 3, 0, 0, "Front part contains a newline character"),

    # Overlapping parts
    ("abc", 0, 2, 2, 0, "Not enough text: the first part and last part overlap or extend beyond the text"),
])
def test_split_errors(text, head, front, back, tail, exc_msg):
    with pytest.raises(ValueError) as exc_info:
        split(text, head, front, back, tail)
    assert exc_msg in str(exc_info.value)


# ======================
# SPECIAL CASE TESTS
# ======================

def test_empty_text():
    """Test empty text with zero parameters"""
    result = split("", 0, 0, 0, 0)
    assert result == TextSplit("", "", "")
    assert result.first + result.middle + result.last == ""


def test_single_character():
    """Test single character text"""
    result = split("a", 0, 1, 0, 0)
    assert result == TextSplit("a", "", "")
    assert result.first + result.middle + result.last == "a"


def test_back_part_with_newline():
    """Test back part containing newline (allowed at end)"""
    result = split("ab\ncd\n", 0, 0, 2, 1)
    assert result == TextSplit("", "a", "b\ncd\n")
    assert result.first + result.middle + result.last == "ab\ncd\n"


def test_front_part_newline_violation():
    """Test front part containing newline (not allowed)"""
    with pytest.raises(ValueError) as exc_info:
        split("ab\ncd\n", 1, 3, 0, 0)
    assert "Front part contains a newline character" in str(exc_info.value)


def test_overlap_edge_case():
    """Test minimal overlap case"""
    with pytest.raises(ValueError) as exc_info:
        split("abc", 0, 2, 2, 0)
    assert "overlap or extend beyond the text" in str(exc_info.value)


def test_full_line_front():
    """Test front part taking entire next line (without newline)"""
    result = split("line1\nline2", 1, 5, 0, 0)
    assert result == TextSplit("line1\nline2", "", "")
    assert result.first + result.middle + result.last == "line1\nline2"


def test_full_line_back():
    """Test back part taking entire previous line (with newline)"""
    result = split("line1\nline2\n", 0, 0, 6, 1)
    assert result == TextSplit("", "", "line1\nline2\n")
    assert result.first + result.middle + result.last == "line1\nline2\n"


def test_last_line_without_newline():
    """Test text without trailing newline"""
    result = split("line1\nline2", 1, 0, 0, 1)
    assert result == TextSplit("line1\n", "", "line2")
    assert result.first + result.middle + result.last == "line1\nline2"