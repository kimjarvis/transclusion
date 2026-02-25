# test_blocks_to_dictionaries.py
import pytest
from src.syncspec.blocks_to_dictionaries import blocks_to_dictionaries


def test_string_passthrough():
    assert blocks_to_dictionaries(['A']) == ['A']
    assert blocks_to_dictionaries(['A', 'B', 'C']) == ['A', 'B', 'C']
    assert blocks_to_dictionaries([]) == []


def test_invalid_item_type():
    with pytest.raises(ValueError, match="Invalid item type"):
        blocks_to_dictionaries([5])
    with pytest.raises(ValueError, match="Invalid item type"):
        blocks_to_dictionaries([None])
    with pytest.raises(ValueError, match="Invalid item type"):
        blocks_to_dictionaries([True])
    with pytest.raises(ValueError, match="Invalid item type"):
        blocks_to_dictionaries([{"key": "value"}])


def test_invalid_sublist_length():
    with pytest.raises(ValueError, match="Invalid sub-list length"):
        blocks_to_dictionaries([['A']])
    with pytest.raises(ValueError, match="Invalid sub-list length"):
        blocks_to_dictionaries([['A', 'B']])
    with pytest.raises(ValueError, match="Invalid sub-list length"):
        blocks_to_dictionaries([['A', 'B', 'C', 'D']])
    with pytest.raises(ValueError, match="Invalid sub-list length"):
        blocks_to_dictionaries([[]])


def test_invalid_list_item():
    with pytest.raises(ValueError, match="Invalid list item"):
        blocks_to_dictionaries([['A', 3, 'C']])
    with pytest.raises(ValueError, match="Invalid list item"):
        blocks_to_dictionaries([[5, 'B', 'C']])
    with pytest.raises(ValueError, match="Invalid list item"):
        blocks_to_dictionaries([['A', 'B', 5]])
    with pytest.raises(ValueError, match="Invalid list item"):
        blocks_to_dictionaries([[None, 'B', 'C']])
    with pytest.raises(ValueError, match="Invalid list item"):
        blocks_to_dictionaries([['A', ['nested'], 'C']])


def test_failed_json_parse():
    with pytest.raises(ValueError, match="Failed to parse JSON"):
        blocks_to_dictionaries([['A', 'B', 'C']])
    with pytest.raises(ValueError, match="Failed to parse JSON"):
        blocks_to_dictionaries([['{invalid}', 'B', '{"valid": true}']])
    with pytest.raises(ValueError, match="Failed to parse JSON"):
        blocks_to_dictionaries([['{"valid": true}', 'B', '{invalid}']])


def test_success_simple():
    json1 = '{  "name": "John Doe" }'
    json2 = '{  "title": "John Doe" }'
    result = blocks_to_dictionaries([[json1, "B", json2]])
    expected = [[
        json1,
        {'name': 'John Doe'},
        'B',
        json2,
        {'title': 'John Doe'}
    ]]
    assert result == expected


def test_success_complex_json():
    json1 = '{"name": "John Doe", "email": "john@example.com", "age": 30, "active": true, "roles": ["admin", "user"], "address": {"street": "123 Main St", "city": "New York", "country": "USA"}, "projects": [{"id": 1, "name": "Website Redesign"}, {"id": 2, "name": "Mobile App"}]}'
    json2 = '{"title": "John Doe"}'

    result = blocks_to_dictionaries([[json1, "B", json2]])

    expected_dict1 = {
        "name": "John Doe",
        "email": "john@example.com",
        "age": 30,
        "active": True,
        "roles": ["admin", "user"],
        "address": {
            "street": "123 Main St",
            "city": "New York",
            "country": "USA"
        },
        "projects": [
            {"id": 1, "name": "Website Redesign"},
            {"id": 2, "name": "Mobile App"}
        ]
    }
    expected_dict2 = {"title": "John Doe"}

    expected = [[json1, expected_dict1, "B", json2, expected_dict2]]
    assert result == expected


def test_mixed_input():
    json_a = '{"x": 1}'
    json_b = '{"y": 2}'
    json_c = '{"a": true}'
    json_d = '{"b": false}'

    input_data = [
        'first string',
        [json_a, 'middle1', json_b],
        'second string',
        [json_c, 'middle2', json_d],
        'third string'
    ]

    expected = [
        'first string',
        [json_a, {"x": 1}, 'middle1', json_b, {"y": 2}],
        'second string',
        [json_c, {"a": True}, 'middle2', json_d, {"b": False}],
        'third string'
    ]

    result = blocks_to_dictionaries(input_data)
    assert result == expected


def test_json_with_unicode():
    json1 = '{"message": "Hello, 世界"}'
    json2 = '{"greeting": "¡Hola!"}'
    input_data = [[json1, 'sep', json2]]
    expected = [[json1, {"message": "Hello, 世界"}, 'sep', json2, {"greeting": "¡Hola!"}]]
    assert blocks_to_dictionaries(input_data) == expected


def test_empty_json_objects():
    input_data = [['{}', 'middle', '{}']]
    expected = [['{}', {}, 'middle', '{}', {}]]
    assert blocks_to_dictionaries(input_data) == expected


def test_multiline_json_strings():
    json1 = """
        {
            "name": "John Doe",
            "email": "john@example.com",
            "age": 30,
            "active": true,
            "roles": ["admin", "user"],
            "address": {
                "street": "123 Main St",
                "city": "New York",
                "country": "USA"
            },
            "projects": [
                {"id": 1, "name": "Website Redesign"},
                {"id": 2, "name": "Mobile App"}
            ]
        }
        """
    json2 = """
        
            "title": "John Doe"

        """
    result = blocks_to_dictionaries([[json1, "B", json2]])

    assert result[0][0] == json1
    assert result[0][1]["name"] == "John Doe"
    assert result[0][1]["email"] == "john@example.com"
    assert result[0][1]["age"] == 30
    assert result[0][1]["active"] is True
    assert result[0][1]["roles"] == ["admin", "user"]
    assert result[0][1]["address"]["city"] == "New York"
    assert len(result[0][1]["projects"]) == 2
    assert result[0][2] == "B"
    assert result[0][3] == json2
    assert result[0][4]["title"] == "John Doe"

def test_pass_through_string():
    assert blocks_to_dictionaries(['A']) == ['A']


def test_invalid_item_type():
    with pytest.raises(ValueError, match="Invalid item type"):
        blocks_to_dictionaries([5])


def test_invalid_sub_list_length():
    with pytest.raises(ValueError, match="Invalid sub-list length"):
        blocks_to_dictionaries([['A']])


def test_invalid_list_item():
    with pytest.raises(ValueError, match="Invalid list item"):
        blocks_to_dictionaries([['A', 3, 'C']])


def test_failed_json_parse():
    with pytest.raises(ValueError, match="Failed to parse JSON"):
        blocks_to_dictionaries([['A', 'B', 'C']])


def test_success_simple():
    result = blocks_to_dictionaries([[
        '{  "name": "John Doe" }',
        "B",
        '{  "title": "John Doe" }'
    ]])
    expected = [[
        '{  "name": "John Doe" }',
        {'name': 'John Doe'},
        'B',
        '{  "title": "John Doe" }',
        {'title': 'John Doe'}
    ]]
    assert result == expected


def test_success_complex_json():
    input_data = [[
        """
{  "name": "John Doe",  "email": "john@example.com",  "age": 30,  "active": true,  "roles": ["admin", "user"],  "address": {    "street": "123 Main St",    "city": "New York",    "country": "USA"  },  "projects": [    {"id": 1, "name": "Website Redesign"},    {"id": 2, "name": "Mobile App"}  ] }
""",
        "B",
        """
{  "title": "John Doe" }
"""]]

    expected = [[
        """
{  "name": "John Doe",  "email": "john@example.com",  "age": 30,  "active": true,  "roles": ["admin", "user"],  "address": {    "street": "123 Main St",    "city": "New York",    "country": "USA"  },  "projects": [    {"id": 1, "name": "Website Redesign"},    {"id": 2, "name": "Mobile App"}  ] }
""",
        {
            "name": "John Doe",
            "email": "john@example.com",
            "age": 30,
            "active": True,
            "roles": ["admin", "user"],
            "address": {
                "street": "123 Main St",
                "city": "New York",
                "country": "USA"
            },
            "projects": [
                {"id": 1, "name": "Website Redesign"},
                {"id": 2, "name": "Mobile App"}
            ]
        },
        "B",
        """
{  "title": "John Doe" }
""",
        {"title": "John Doe"}
    ]]

    assert blocks_to_dictionaries(input_data) == expected


def test_braces_added_to_first_item():
    """Test that unbraced JSON in first position gets wrapped and parsed."""
    input_data = [[
        """
            "title": "John Doe"
        """,
        "B",
        """
            { "status": "active" }
        """
    ]]

    result = blocks_to_dictionaries(input_data)

    assert result[0][1] == {"title": "John Doe"}
    assert result[0][4] == {"status": "active"}


def test_braces_added_to_third_item():
    """Test that unbraced JSON in third position gets wrapped and parsed."""
    input_data = [[
        """
            { "name": "Alice" }
        """,
        "M",
        """
            "role": "admin", "level": 5
        """
    ]]

    result = blocks_to_dictionaries(input_data)

    assert result[0][1] == {"name": "Alice"}
    assert result[0][4] == {"role": "admin", "level": 5}


def test_braces_added_to_both_items():
    """Test that both first and third items get braces added when needed."""
    input_data = [[
        '"type": "Uppercase"',
        "X",
        '"value": 42'
    ]]

    result = blocks_to_dictionaries(input_data)

    assert result[0][1] == {"type": "Uppercase"}
    assert result[0][4] == {"value": 42}


def test_braces_added_with_whitespace():
    """Test brace wrapping handles leading/trailing whitespace correctly."""
    input_data = [[
        """
            "key": "value"
        """,
        "sep",
        """
                "nested": {"a": 1}
        """
    ]]

    result = blocks_to_dictionaries(input_data)

    assert result[0][1] == {"key": "value"}
    assert result[0][4] == {"nested": {"a": 1}}