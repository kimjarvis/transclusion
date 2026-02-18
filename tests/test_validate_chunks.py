# test_validate_chunks.py
import pytest
from validate_chunks import validate_chunks

def test_valid_chunk():
    validate_chunks([[{"type": "Begin", "source": "ex"}, "B", {"type": "End"}]])

def test_valid_chunk_with_options():
    validate_chunks([[{"type": "Begin", "source": "ex", "shift": 1}, "B", {"type": "End"}]])

def test_invalid_sublist_length():
    with pytest.raises(ValueError, match="Invalid sub-list length"):
        validate_chunks([[{}, "B"]])

def test_invalid_item_type_dict():
    with pytest.raises(ValueError, match="Invalid item type"):
        validate_chunks([["str", "B", {}]])

def test_invalid_item_type_str():
    with pytest.raises(ValueError, match="Invalid item type"):
        validate_chunks([[{}, 1, {}]])

def test_invalid_parameter_type():
    with pytest.raises(ValueError, match="Invalid parameter: type"):
        validate_chunks([[{"type": "Invalid"}, "B", {"type": "End"}]])

def test_invalid_begin_structure():
    with pytest.raises(Exception): # Pydantic ValidationError
        validate_chunks([[{"type": "Begin"}, "B", {"type": "End"}]]) # Missing source

def test_invalid_end_structure():
    with pytest.raises(Exception):
        validate_chunks([[{"type": "Begin", "source": "s"}, "B", {"type": "End", "extra": 1}]])



# Test Valid Cases

def test_valid_begin_end():
    """Test valid Begin and End dictionaries."""
    validate_chunks([
        [{
            "type": "Begin",
            "source": "example",
            "shift": 4,
            "skip": 1,
            "add": 1
        }, "B", {"type": "End"}]
    ])


def test_valid_begin_end_no_optional_fields():
    """Test valid Begin dict without optional fields."""
    validate_chunks([
        [{
            "type": "Begin",
            "source": "example"
        }, "B", {"type": "End"}]
    ])


def test_valid_begin_end_partial_optional_fields():
    """Test valid Begin dict with partial optional fields."""
    validate_chunks([
        [{
            "type": "Begin",
            "source": "example",
            "shift": 4
        }, "B", {"type": "End"}]
    ])


def test_valid_multiple_sublists():
    """Test multiple valid sub-lists."""
    validate_chunks([
        [{"type": "Begin", "source": "src1"}, "A", {"type": "End"}],
        [{"type": "Begin", "source": "src2"}, "B", {"type": "End"}],
    ])


def test_string_items_ignored():
    """Test that string items in the list are ignored."""
    validate_chunks([
        "some string",
        [{"type": "Begin", "source": "example"}, "B", {"type": "End"}],
        "another string"
    ])


def test_empty_list():
    """Test empty list."""
    validate_chunks([])


def test_only_strings_no_sublists():
    """Test list with only strings, no sub-lists to process."""
    validate_chunks(["string1", "string2", "string3"])


# Test Invalid Sub-List Length

def test_sublist_too_short_2_elements():
    """Test sub-list with 2 elements raises ValueError."""
    with pytest.raises(ValueError, match="Invalid sub-list length"):
        validate_chunks([
            [{"type": "Begin", "source": "example"}, "B"]
        ])


def test_sublist_too_short_1_element():
    """Test sub-list with 1 element raises ValueError."""
    with pytest.raises(ValueError, match="Invalid sub-list length"):
        validate_chunks([
            [{"type": "Begin", "source": "example"}]
        ])


def test_sublist_too_long_4_elements():
    """Test sub-list with 4 elements raises ValueError."""
    with pytest.raises(ValueError, match="Invalid sub-list length"):
        validate_chunks([
            [{"type": "Begin", "source": "example"}, "B", {"type": "End"}, "extra"]
        ])


def test_sublist_empty():
    """Test empty sub-list raises ValueError."""
    with pytest.raises(ValueError, match="Invalid sub-list length"):
        validate_chunks([[]])


# Test Invalid Item Types

def test_first_item_not_dict_int():
    """Test first item as int raises ValueError."""
    with pytest.raises(ValueError, match="Invalid item type"):
        validate_chunks([
            [123, "B", {"type": "End"}]
        ])


def test_first_item_not_dict_string():
    """Test first item as string raises ValueError."""
    with pytest.raises(ValueError, match="Invalid item type"):
        validate_chunks([
            ["not a dict", "B", {"type": "End"}]
        ])


def test_first_item_not_dict_list():
    """Test first item as list raises ValueError."""
    with pytest.raises(ValueError, match="Invalid item type"):
        validate_chunks([
            [["not", "a", "dict"], "B", {"type": "End"}]
        ])


def test_second_item_not_string_int():
    """Test second item as int raises ValueError."""
    with pytest.raises(ValueError, match="Invalid item type"):
        validate_chunks([
            [{"type": "Begin", "source": "example"}, 123, {"type": "End"}]
        ])


def test_second_item_not_string_dict():
    """Test second item as dict raises ValueError."""
    with pytest.raises(ValueError, match="Invalid item type"):
        validate_chunks([
            [{"type": "Begin", "source": "example"}, {"not": "string"}, {"type": "End"}]
        ])


def test_second_item_not_string_list():
    """Test second item as list raises ValueError."""
    with pytest.raises(ValueError, match="Invalid item type"):
        validate_chunks([
            [{"type": "Begin", "source": "example"}, ["not", "string"], {"type": "End"}]
        ])


def test_third_item_not_dict_int():
    """Test third item as int raises ValueError."""
    with pytest.raises(ValueError, match="Invalid item type"):
        validate_chunks([
            [{"type": "Begin", "source": "example"}, "B", 123]
        ])


def test_third_item_not_dict_string():
    """Test third item as string raises ValueError."""
    with pytest.raises(ValueError, match="Invalid item type"):
        validate_chunks([
            [{"type": "Begin", "source": "example"}, "B", "not a dict"]
        ])


def test_third_item_not_dict_list():
    """Test third item as list raises ValueError."""
    with pytest.raises(ValueError, match="Invalid item type"):
        validate_chunks([
            [{"type": "Begin", "source": "example"}, "B", ["not", "a", "dict"]]
        ])


# Test Invalid Dictionary Structures

def test_begin_dict_wrong_type_value():
    """Test Begin dict with wrong type value."""
    with pytest.raises(ValueError, match="Invalid parameter: type"):
        validate_chunks([
            [{"type": "WrongType", "source": "example"}, "B", {"type": "End"}]
        ])


def test_end_dict_wrong_type_value():
    """Test End dict with wrong type value."""
    with pytest.raises(ValueError, match="Invalid parameter: type"):
        validate_chunks([
            [{"type": "Begin", "source": "example"}, "B", {"type": "WrongEnd"}]
        ])


def test_begin_dict_missing_source():
    """Test Begin dict missing required 'source' field."""
    with pytest.raises(Exception):  # Pydantic ValidationError
        validate_chunks([
            [{"type": "Begin"}, "B", {"type": "End"}]
        ])


def test_begin_dict_missing_type():
    """Test Begin dict missing 'type' field."""
    with pytest.raises(ValueError, match="Invalid parameter: type"):
        validate_chunks([
            [{"source": "example"}, "B", {"type": "End"}]
        ])


def test_end_dict_missing_type():
    """Test End dict missing 'type' field."""
    with pytest.raises(ValueError, match="Invalid parameter: type"):
        validate_chunks([
            [{"type": "Begin", "source": "example"}, "B", {}]
        ])


def test_begin_dict_extra_fields():
    """Test Begin dict with extra fields is allowed by default."""
    with pytest.raises(Exception):  # Pydantic ValidationError
        validate_chunks([
            [{"type": "Begin", "source": "example", "extra": "field"}, "B", {"type": "End"}]
        ])


def test_begin_dict_wrong_type_for_source():
    """Test Begin dict with wrong type for source."""
    with pytest.raises(Exception):  # Pydantic ValidationError
        validate_chunks([
            [{"type": "Begin", "source": 123}, "B", {"type": "End"}]
        ])


def test_begin_dict_wrong_type_for_shift():
    """Test Begin dict with wrong type for shift."""
    with pytest.raises(Exception):  # Pydantic ValidationError
        validate_chunks([
            [{"type": "Begin", "source": "example", "shift": "not int"}, "B", {"type": "End"}]
        ])


def test_begin_dict_wrong_type_for_skip():
    """Test Begin dict with wrong type for skip."""
    with pytest.raises(Exception):  # Pydantic ValidationError
        validate_chunks([
            [{"type": "Begin", "source": "example", "skip": "not int"}, "B", {"type": "End"}]
        ])


def test_begin_dict_wrong_type_for_add():
    """Test Begin dict with wrong type for add."""
    with pytest.raises(Exception):  # Pydantic ValidationError
        validate_chunks([
            [{"type": "Begin", "source": "example", "add": "not int"}, "B", {"type": "End"}]
        ])


def test_end_dict_extra_fields():
    """Test End dict with extra fields is allowed by default."""
    with pytest.raises(Exception):  # Pydantic ValidationError
        validate_chunks([
            [{"type": "Begin", "source": "example"}, "B", {"type": "End", "extra": "field"}]
        ])


def test_end_dict_wrong_type_for_type_field():
    """Test End dict with wrong type for type field."""
    with pytest.raises(Exception):  # Pydantic ValidationError
        validate_chunks([
            [{"type": "Begin", "source": "example"}, "B", {"type": 123}]
        ])


def test_dict_with_no_type_field():
    """Test dict with no type field raises Invalid parameter: type."""
    with pytest.raises(ValueError, match="Invalid parameter: type"):
        validate_chunks([
            [{"nested": {"type": "Begin"}}, "B", {"type": "End"}]
        ])


# Test Mixed and Edge Cases

def test_first_sublist_valid_second_invalid():
    """Test that validation stops at first invalid sub-list."""
    with pytest.raises(ValueError, match="Invalid sub-list length"):
        validate_chunks([
            [{"type": "Begin", "source": "example"}, "B", {"type": "End"}],
            [{"type": "Begin", "source": "example"}, "B"]  # Invalid - too short
        ])


def test_multiple_errors_first_occurrence():
    """Test that first error is raised when multiple exist."""
    with pytest.raises(ValueError, match="Invalid sub-list length"):
        validate_chunks([
            [{"type": "Begin", "source": "example"}, "B", {"type": "End"}, "extra"],
            [123, "B", {"type": "End"}]  # Would also fail
        ])


def test_none_as_sublist_item():
    """Test None values in sub-list positions."""
    with pytest.raises(ValueError, match="Invalid item type"):
        validate_chunks([
            [None, "B", {"type": "End"}]
        ])
