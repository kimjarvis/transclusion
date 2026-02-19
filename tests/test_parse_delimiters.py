from src.transclusion.parse_delimiters import parse_delimiters


def test_single_character():
    """Test with a single character and no delimiters"""
    assert parse_delimiters("A") == ["A"]

def test_single_word_no_delimiters():
    """Test with a word and no delimiters"""
    assert parse_delimiters("Hello") == ["Hello"]

def test_delimiters_in_middle():
    """Test with delimiters in the middle of text"""
    assert parse_delimiters("A{{B}}C") == ["A", "B", "C"]

def test_start_with_delimiters():
    """Test when string starts with delimiters"""
    assert parse_delimiters("{{B}}C") == ["", "B", "C"]

def test_end_with_delimiters():
    """Test when string ends with delimiters"""
    assert parse_delimiters("{{B}}") == ["", "B", ""]

def test_multiple_delimiters_pairs():
    """Test with multiple delimiters pairs"""
    assert parse_delimiters("A{{B}}C{{D}}E") == ["A", "B", "C", "D", "E"]

def test_consecutive_delimiters():
    """Test with consecutive delimiters pairs"""
    assert parse_delimiters("A{{B}}{{D}}E") == ["A", "B", "", "D", "E"]

def test_empty_delimiters():
    """Test with empty delimiters"""
    assert parse_delimiters("A{{}}C{{}}") == ["A", "", "C", "", ""]

def test_only_delimiters():
    """Test with only delimiters and no text"""
    assert parse_delimiters("{{}}") == ["", "", ""]

def test_custom_delimiters():
    """Test with custom delimiters"""
    assert parse_delimiters("A<B>C", "<", ">") == ["A", "B", "C"]
    assert parse_delimiters("<B>C", "<", ">") == ["", "B", "C"]
    assert parse_delimiters("<B>", "<", ">") == ["", "B", ""]
    assert parse_delimiters("A<B><D>E", "<", ">") == ["A", "B", "", "D", "E"]

def test_longer_delimiters():
    """Test with longer delimiter strings"""
    assert parse_delimiters("A[[]B[]]C", "[[]", "[]]") == ["A", "B", "C"]
    assert parse_delimiters("[[]B[]]C", "[[]", "[]]") == ["", "B", "C"]
    assert parse_delimiters("[[]B[]]", "[[]", "[]]") == ["", "B", ""]

def test_empty_string():
    """Test with empty string"""
    assert parse_delimiters("") == [""]

def test_multibyte_characters():
    """Test with multibyte characters"""
    assert parse_delimiters("你好{{世界}}！") == ["你好", "世界", "！"]

def test_whitespace_handling():
    """Test with whitespace in the text"""
    assert parse_delimiters("  {{  }}  ") == ["  ", "  ", "  "]

def test_complex_scenario():
    """Test a more complex scenario"""
    result = parse_delimiters("pre{{first}}mid{{second}}post")
    assert result == ["pre", "first", "mid", "second", "post"]