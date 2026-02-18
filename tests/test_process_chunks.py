# test_process_chunks.py
import pytest
from process_chunks import process_chunks


def test_string_passthrough():
    assert process_chunks(['A']) == ['A']
    assert process_chunks(['A', 'B', 'C']) == ['A', 'B', 'C']
    assert process_chunks([]) == []


def test_invalid_item_type():
    with pytest.raises(ValueError, match="Invalid item type"):
        process_chunks([5])
    with pytest.raises(ValueError, match="Invalid item type"):
        process_chunks([None])
    with pytest.raises(ValueError, match="Invalid item type"):
        process_chunks([True])
    with pytest.raises(ValueError, match="Invalid item type"):
        process_chunks([{"key": "value"}])


def test_invalid_sublist_length():
    with pytest.raises(ValueError, match="Invalid sub-list length"):
        process_chunks([['A']])
    with pytest.raises(ValueError, match="Invalid sub-list length"):
        process_chunks([['A', 'B']])
    with pytest.raises(ValueError, match="Invalid sub-list length"):
        process_chunks([['A', 'B', 'C', 'D']])
    with pytest.raises(ValueError, match="Invalid sub-list length"):
        process_chunks([[]])


def test_invalid_list_item():
    with pytest.raises(ValueError, match="Invalid list item"):
        process_chunks([['A', 3, 'C']])
    with pytest.raises(ValueError, match="Invalid list item"):
        process_chunks([[5, 'B', 'C']])
    with pytest.raises(ValueError, match="Invalid list item"):
        process_chunks([['A', 'B', 5]])
    with pytest.raises(ValueError, match="Invalid list item"):
        process_chunks([[None, 'B', 'C']])
    with pytest.raises(ValueError, match="Invalid list item"):
        process_chunks([['A', ['nested'], 'C']])


def test_failed_json_parse():
    with pytest.raises(ValueError, match="Failed to parse JSON"):
        process_chunks([['A', 'B', 'C']])
    with pytest.raises(ValueError, match="Failed to parse JSON"):
        process_chunks([['{invalid}', 'B', '{"valid": true}']])
    with pytest.raises(ValueError, match="Failed to parse JSON"):
        process_chunks([['{"valid": true}', 'B', '{invalid}']])


def test_success_simple():
    json1 = '{  "name": "John Doe" }'
    json2 = '{  "title": "John Doe" }'
    result = process_chunks([[json1, "B", json2]])
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

    result = process_chunks([[json1, "B", json2]])

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

    result = process_chunks(input_data)
    assert result == expected


def test_json_with_unicode():
    json1 = '{"message": "Hello, 世界"}'
    json2 = '{"greeting": "¡Hola!"}'
    input_data = [[json1, 'sep', json2]]
    expected = [[json1, {"message": "Hello, 世界"}, 'sep', json2, {"greeting": "¡Hola!"}]]
    assert process_chunks(input_data) == expected


def test_empty_json_objects():
    input_data = [['{}', 'middle', '{}']]
    expected = [['{}', {}, 'middle', '{}', {}]]
    assert process_chunks(input_data) == expected


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
        {
            "title": "John Doe"
        }
        """
    result = process_chunks([[json1, "B", json2]])

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
    assert process_chunks(['A']) == ['A']


def test_invalid_item_type():
    with pytest.raises(ValueError, match="Invalid item type"):
        process_chunks([5])


def test_invalid_sub_list_length():
    with pytest.raises(ValueError, match="Invalid sub-list length"):
        process_chunks([['A']])


def test_invalid_list_item():
    with pytest.raises(ValueError, match="Invalid list item"):
        process_chunks([['A', 3, 'C']])


def test_failed_json_parse():
    with pytest.raises(ValueError, match="Failed to parse JSON"):
        process_chunks([['A', 'B', 'C']])


def test_success_simple():
    result = process_chunks([[
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

    assert process_chunks(input_data) == expected

