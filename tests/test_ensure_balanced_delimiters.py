import pytest
from ensure_balanced_delimiters import ensure_balanced_delimiters

class TestEnsureBalancedParentheses:

    def test_empty_string(self):
        """Test that empty string passes validation"""
        ensure_balanced_delimiters("")

    def test_valid_simple_case(self):
        """Test valid case with spaces"""
        ensure_balanced_delimiters("{{ }}")

    def test_valid_no_spaces(self):
        """Test valid case without spaces"""
        ensure_balanced_delimiters("{{}}")

    def test_valid_with_text(self):
        """Test valid case with text between delimiters"""
        ensure_balanced_delimiters("{{ hello world }}")

    def test_valid_multiple_pairs(self):
        """Test valid case with multiple separate delimiters pairs"""
        ensure_balanced_delimiters("{{first}} {{second}}")

    def test_valid_with_special_characters(self):
        """Test valid case with special characters"""
        ensure_balanced_delimiters("{{ !@#$%^&*() }}")

    def test_nested_delimiters_raises_error(self):
        """Test that nested delimiters raise ValueError"""
        with pytest.raises(ValueError, match="Parentheses cannot be nested"):
            ensure_balanced_delimiters("{{ {{ }} }}")

    def test_nested_with_unclosed_raises_nesting_error(self):
        """Test that nested delimiters take precedence over unbalanced check"""
        with pytest.raises(ValueError, match="Parentheses cannot be nested"):
            ensure_balanced_delimiters("{{ {{ }}")  # This is nested first, then unbalanced

    def test_unmatched_opening_raises_error(self):
        """Test that unmatched opening delimiters raise ValueError"""
        with pytest.raises(ValueError, match="Parentheses are not matched"):
            ensure_balanced_delimiters("{{ hello")

    def test_unmatched_closing_raises_error(self):
        """Test that unmatched closing delimiters raise ValueError"""
        with pytest.raises(ValueError, match="Parentheses are not matched"):
            ensure_balanced_delimiters("hello }}")

    def test_only_opening_raises_error(self):
        """Test that only opening delimiters raise ValueError"""
        with pytest.raises(ValueError, match="Parentheses are not matched"):
            ensure_balanced_delimiters("{{")

    def test_only_closing_raises_error(self):
        """Test that only closing delimiters raise ValueError"""
        with pytest.raises(ValueError, match="Parentheses are not matched"):
            ensure_balanced_delimiters("}}")

    def test_custom_delimiters_different_check(self):
        """Test that using same custom delimiters raises error"""
        with pytest.raises(ValueError, match="Opening and closing delimiters must be different"):
            ensure_balanced_delimiters("test", "##", "##")

    def test_custom_delimiters_character_overlap(self):
        """Test that overlapping delimiters characters raise error"""
        with pytest.raises(ValueError,
                           match="The last character of open_delimiter cannot be the same as the first character of close_delimiter"):
            ensure_balanced_delimiters("test", "[{", "{]")

    def test_custom_delimiters_valid(self):
        """Test valid case with custom delimiters"""
        ensure_balanced_delimiters("<< hello >>", "<<", ">>")

    def test_custom_delimiters_with_different_lengths(self):
        """Test valid case with custom delimiters of different lengths"""
        ensure_balanced_delimiters("((hello))", "(((", ")))")

    def test_complex_valid_case(self):
        """Test complex valid case with multiple tokens"""
        ensure_balanced_delimiters("{{ token1 }} text {{ token2 }} more text {{ token3 }}")

    def test_incomplete_opening_doesnt_match(self):
        """Test that incomplete delimiters don't trigger matches"""
        ensure_balanced_delimiters("{ hello }")  # Single braces shouldn't match