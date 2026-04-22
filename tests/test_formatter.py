import json
from gendiff.formatter import plain, json_formatter
from gendiff.diff_builder import DiffNode, DiffStatus


def test_plain_added_property():
    """Тестирует форматирование добавленного свойства."""
    diff = {
        "verbose": DiffNode(
            key="verbose",
            status=DiffStatus.ADDED,
            new_value=True
        )
    }
    
    result = plain(diff)
    expected = "Property 'verbose' was added with value: true"
    
    assert result == expected


def test_plain_removed_property():
    """Тестирует форматирование удаленного свойства."""
    diff = {
        "timeout": DiffNode(
            key="timeout",
            status=DiffStatus.REMOVED,
            old_value=50
        )
    }
    
    result = plain(diff)
    expected = "Property 'timeout' was removed"
    
    assert result == expected


def test_plain_changed_property():
    """Тестирует форматирование измененного свойства."""
    diff = {
        "host": DiffNode(
            key="host",
            status=DiffStatus.CHANGED,
            old_value="localhost",
            new_value="hexlet.io"
        )
    }
    
    result = plain(diff)
    expected = "Property 'host' was updated. From 'localhost' to 'hexlet.io'"
    
    assert result == expected


def test_plain_added_complex_value():
    """Тестирует форматирование добавленного сложного значения."""
    diff = {
        "settings": DiffNode(
            key="settings",
            status=DiffStatus.ADDED,
            new_value={"timeout": 30, "retry": 3}
        )
    }
    
    result = plain(diff)
    expected = "Property 'settings' was added with value: [complex value]"
    
    assert result == expected


def test_plain_changed_to_complex_value():
    """Тестирует форматирование изменения на сложное значение."""
    diff = {
        "config": DiffNode(
            key="config",
            status=DiffStatus.CHANGED,
            old_value="simple",
            new_value={"nested": {"key": "value"}}
        )
    }
    result = plain(diff)
    assert result == (
        "Property 'config' was updated. From 'simple' to [complex value]"
    )


def test_plain_changed_from_complex_value():
    """Тестирует форматирование изменения со сложного значения."""
    diff = {
        "data": DiffNode(
            key="data",
            status=DiffStatus.CHANGED,
            old_value={"old": "structure"},
            new_value="new value"
        )
    }
    
    result = plain(diff)
    assert result == (
        "Property 'data' was updated. From [complex value] to 'new value'"
    )


def test_plain_nested_structure():
    """Тестирует форматирование вложенной структуры."""
    diff = {
        "common": DiffNode(
            key="common",
            status=DiffStatus.NESTED,
            children={
                "setting1": DiffNode(
                    key="setting1",
                    status=DiffStatus.ADDED,
                    new_value="value"
                ),
                "setting2": DiffNode(
                    key="setting2",
                    status=DiffStatus.CHANGED,
                    old_value=100,
                    new_value=200
                ),
                "setting3": DiffNode(
                    key="setting3",
                    status=DiffStatus.REMOVED,
                    old_value=True
                )
            }
        )
    }
    
    result = plain(diff)
    lines = result.split('\n')
    
    assert "Property 'common.setting1' was added with value: 'value'" in lines
    assert "Property 'common.setting2' was updated. From 100 to 200" in lines
    assert "Property 'common.setting3' was removed" in lines


def test_plain_multiple_properties():
    """Тестирует форматирование нескольких свойств."""
    diff = {
        "host": DiffNode(
            key="host",
            status=DiffStatus.UNCHANGED,
            old_value="hexlet.io"
        ),
        "timeout": DiffNode(
            key="timeout",
            status=DiffStatus.CHANGED,
            old_value=50,
            new_value=20
        ),
        "verbose": DiffNode(
            key="verbose",
            status=DiffStatus.ADDED,
            new_value=True
        ),
        "proxy": DiffNode(
            key="proxy",
            status=DiffStatus.REMOVED,
            old_value="123.234.53.22"
        )
    }
    
    result = plain(diff)
    lines = result.split('\n')
    
    assert "Property 'timeout' was updated. From 50 to 20" in lines
    assert "Property 'verbose' was added with value: true" in lines
    assert "Property 'proxy' was removed" in lines
    # Unchanged properties should not appear in plain format
    assert "host" not in result


def test_plain_empty_diff():
    """Тестирует форматирование пустого diff."""
    diff = {}
    
    result = plain(diff)
    expected = ""
    
    assert result == expected


def test_plain_only_unchanged():
    """Тестирует форматирование diff с только неизмененными свойствами."""
    diff = {
        "host": DiffNode(
            key="host",
            status=DiffStatus.UNCHANGED,
            old_value="hexlet.io"
        ),
        "timeout": DiffNode(
            key="timeout",
            status=DiffStatus.UNCHANGED,
            old_value=50
        )
    }
    
    result = plain(diff)
    expected = ""
    
    assert result == expected


def test_plain_different_value_types():
    """Тестирует форматирование различных типов значений."""
    diff = {
        "string_prop": DiffNode(
            key="string_prop",
            status=DiffStatus.ADDED,
            new_value="test string"
        ),
        "int_prop": DiffNode(
            key="int_prop",
            status=DiffStatus.ADDED,
            new_value=42
        ),
        "float_prop": DiffNode(
            key="float_prop",
            status=DiffStatus.ADDED,
            new_value=3.14
        ),
        "bool_prop": DiffNode(
            key="bool_prop",
            status=DiffStatus.ADDED,
            new_value=True
        ),
        "null_prop": DiffNode(
            key="null_prop",
            status=DiffStatus.ADDED,
            new_value=None
        ),
        "list_prop": DiffNode(
            key="list_prop",
            status=DiffStatus.ADDED,
            new_value=[1, 2, 3]
        )
    }
    
    result = plain(diff)
    lines = result.split('\n')
    
    assert "Property 'string_prop' was added with value: 'test string'" in lines
    assert "Property 'int_prop' was added with value: 42" in lines
    assert "Property 'float_prop' was added with value: 3.14" in lines
    assert "Property 'bool_prop' was added with value: true" in lines
    assert "Property 'null_prop' was added with value: null" in lines
    assert (
        "Property 'list_prop' was added with value: [complex value]" in lines
    )


def test_plain_deeply_nested():
    """Тестирует форматирование глубоко вложенной структуры."""
    diff = {
        "database": DiffNode(
            key="database",
            status=DiffStatus.NESTED,
            children={
                "credentials": DiffNode(
                    key="credentials",
                    status=DiffStatus.NESTED,
                    children={
                        "password": DiffNode(
                            key="password",
                            status=DiffStatus.CHANGED,
                            old_value="secret",
                            new_value="new-secret"
                        )
                    }
                )
            }
        )
    }
    
    result = plain(diff)
    assert result == (
        "Property 'database.credentials.password' was updated. "
        "From 'secret' to 'new-secret'"
    )


def test_plain_mixed_nested_and_simple():
    """Тестирует смешанные вложенные и простые изменения."""
    diff = {
        "setting1": DiffNode(
            key="setting1",
            status=DiffStatus.CHANGED,
            old_value="old",
            new_value="new"
        ),
        "nested": DiffNode(
            key="nested",
            status=DiffStatus.NESTED,
            children={
                "prop1": DiffNode(
                    key="prop1",
                    status=DiffStatus.ADDED,
                    new_value="value1"
                ),
                "deep": DiffNode(
                    key="deep",
                    status=DiffStatus.NESTED,
                    children={
                        "prop2": DiffNode(
                            key="prop2",
                            status=DiffStatus.REMOVED,
                            old_value="value2"
                        )
                    }
                )
            }
        )
    }
    
    result = plain(diff)
    lines = result.split('\n')
    
    assert "Property 'setting1' was updated. From 'old' to 'new'" in lines
    assert "Property 'nested.prop1' was added with value: 'value1'" in lines
    assert "Property 'nested.deep.prop2' was removed" in lines


def test_plain_complex_changed_values():
    """Тестирует изменение сложных значений."""
    diff = {
        "dict1": DiffNode(
            key="dict1",
            status=DiffStatus.CHANGED,
            old_value={"a": 1, "b": 2},
            new_value={"c": 3, "d": 4}
        ),
        "list1": DiffNode(
            key="list1",
            status=DiffStatus.CHANGED,
            old_value=[1, 2, 3],
            new_value=[4, 5, 6]
        )
    }
    
    result = plain(diff)
    lines = result.split('\n')
    
    assert (
        "Property 'dict1' was updated. From [complex value] to [complex value]"
        in lines
    )
    assert (
        "Property 'list1' was updated. From [complex value] to [complex value]"
        in lines
    )


def test_json_added_property():
    """Тестирует JSON форматирование добавленного свойства."""
    diff = {
        "verbose": DiffNode(
            key="verbose",
            status=DiffStatus.ADDED,
            new_value=True
        )
    }
    
    result = json_formatter(diff)
    parsed = json.loads(result)
    
    expected = {
        "verbose": {
            "status": "added",
            "value": True
        }
    }
    
    assert parsed == expected


def test_json_removed_property():
    """Тестирует JSON форматирование удаленного свойства."""
    diff = {
        "timeout": DiffNode(
            key="timeout",
            status=DiffStatus.REMOVED,
            old_value=50
        )
    }
    
    result = json_formatter(diff)
    parsed = json.loads(result)
    
    expected = {
        "timeout": {
            "status": "removed",
            "value": 50
        }
    }
    
    assert parsed == expected


def test_json_changed_property():
    """Тестирует JSON форматирование измененного свойства."""
    diff = {
        "host": DiffNode(
            key="host",
            status=DiffStatus.CHANGED,
            old_value="localhost",
            new_value="hexlet.io"
        )
    }
    
    result = json_formatter(diff)
    parsed = json.loads(result)
    
    expected = {
        "host": {
            "status": "changed",
            "old_value": "localhost",
            "new_value": "hexlet.io"
        }
    }
    
    assert parsed == expected


def test_json_unchanged_property():
    """Тестирует JSON форматирование неизмененного свойства."""
    diff = {
        "host": DiffNode(
            key="host",
            status=DiffStatus.UNCHANGED,
            old_value="hexlet.io"
        )
    }
    
    result = json_formatter(diff)
    parsed = json.loads(result)
    
    expected = {
        "host": {
            "status": "unchanged",
            "value": "hexlet.io"
        }
    }
    
    assert parsed == expected


def test_json_nested_structure():
    """Тестирует JSON форматирование вложенной структуры."""
    diff = {
        "common": DiffNode(
            key="common",
            status=DiffStatus.NESTED,
            children={
                "setting1": DiffNode(
                    key="setting1",
                    status=DiffStatus.ADDED,
                    new_value="value"
                ),
                "setting2": DiffNode(
                    key="setting2",
                    status=DiffStatus.CHANGED,
                    old_value=100,
                    new_value=200
                ),
                "setting3": DiffNode(
                    key="setting3",
                    status=DiffStatus.REMOVED,
                    old_value=True
                )
            }
        )
    }
    
    result = json_formatter(diff)
    parsed = json.loads(result)
    
    expected = {
        "common": {
            "status": "nested",
            "children": {
                "setting1": {
                    "status": "added",
                    "value": "value"
                },
                "setting2": {
                    "status": "changed",
                    "old_value": 100,
                    "new_value": 200
                },
                "setting3": {
                    "status": "removed",
                    "value": True
                }
            }
        }
    }
    
    assert parsed == expected


def test_json_multiple_properties():
    """Тестирует JSON форматирование нескольких свойств."""
    diff = {
        "host": DiffNode(
            key="host",
            status=DiffStatus.UNCHANGED,
            old_value="hexlet.io"
        ),
        "timeout": DiffNode(
            key="timeout",
            status=DiffStatus.CHANGED,
            old_value=50,
            new_value=20
        ),
        "verbose": DiffNode(
            key="verbose",
            status=DiffStatus.ADDED,
            new_value=True
        ),
        "proxy": DiffNode(
            key="proxy",
            status=DiffStatus.REMOVED,
            old_value="123.234.53.22"
        )
    }
    
    result = json_formatter(diff)
    parsed = json.loads(result)
    
    expected = {
        "host": {
            "status": "unchanged",
            "value": "hexlet.io"
        },
        "proxy": {
            "status": "removed",
            "value": "123.234.53.22"
        },
        "timeout": {
            "status": "changed",
            "old_value": 50,
            "new_value": 20
        },
        "verbose": {
            "status": "added",
            "value": True
        }
    }
    
    assert parsed == expected


def test_json_empty_diff():
    """Тестирует JSON форматирование пустого diff."""
    diff = {}
    
    result = json_formatter(diff)
    parsed = json.loads(result)
    
    expected = {}
    
    assert parsed == expected


def test_json_different_value_types():
    """Тестирует JSON форматирование различных типов значений."""
    diff = {
        "string_prop": DiffNode(
            key="string_prop",
            status=DiffStatus.ADDED,
            new_value="test string"
        ),
        "int_prop": DiffNode(
            key="int_prop",
            status=DiffStatus.ADDED,
            new_value=42
        ),
        "float_prop": DiffNode(
            key="float_prop",
            status=DiffStatus.ADDED,
            new_value=3.14
        ),
        "bool_prop": DiffNode(
            key="bool_prop",
            status=DiffStatus.ADDED,
            new_value=True
        ),
        "null_prop": DiffNode(
            key="null_prop",
            status=DiffStatus.ADDED,
            new_value=None
        ),
        "list_prop": DiffNode(
            key="list_prop",
            status=DiffStatus.ADDED,
            new_value=[1, 2, 3]
        ),
        "dict_prop": DiffNode(
            key="dict_prop",
            status=DiffStatus.ADDED,
            new_value={"key": "value"}
        )
    }
    
    result = json_formatter(diff)
    parsed = json.loads(result)
    
    expected = {
        "bool_prop": {
            "status": "added",
            "value": True
        },
        "dict_prop": {
            "status": "added",
            "value": {"key": "value"}
        },
        "float_prop": {
            "status": "added",
            "value": 3.14
        },
        "int_prop": {
            "status": "added",
            "value": 42
        },
        "list_prop": {
            "status": "added",
            "value": [1, 2, 3]
        },
        "null_prop": {
            "status": "added",
            "value": None
        },
        "string_prop": {
            "status": "added",
            "value": "test string"
        }
    }
    
    assert parsed == expected


def test_json_deeply_nested():
    """Тестирует JSON форматирование глубоко вложенной структуры."""
    diff = {
        "database": DiffNode(
            key="database",
            status=DiffStatus.NESTED,
            children={
                "credentials": DiffNode(
                    key="credentials",
                    status=DiffStatus.NESTED,
                    children={
                        "password": DiffNode(
                            key="password",
                            status=DiffStatus.CHANGED,
                            old_value="secret",
                            new_value="new-secret"
                        )
                    }
                )
            }
        )
    }
    
    result = json_formatter(diff)
    parsed = json.loads(result)
    
    expected = {
        "database": {
            "status": "nested",
            "children": {
                "credentials": {
                    "status": "nested",
                    "children": {
                        "password": {
                            "status": "changed",
                            "old_value": "secret",
                            "new_value": "new-secret"
                        }
                    }
                }
            }
        }
    }
    
    assert parsed == expected


def test_json_complex_changed_values():
    """Тестирует JSON форматирование изменения сложных значений."""
    diff = {
        "dict1": DiffNode(
            key="dict1",
            status=DiffStatus.CHANGED,
            old_value={"a": 1, "b": 2},
            new_value={"c": 3, "d": 4}
        ),
        "list1": DiffNode(
            key="list1",
            status=DiffStatus.CHANGED,
            old_value=[1, 2, 3],
            new_value=[4, 5, 6]
        )
    }
    
    result = json_formatter(diff)
    parsed = json.loads(result)
    
    expected = {
        "dict1": {
            "status": "changed",
            "old_value": {"a": 1, "b": 2},
            "new_value": {"c": 3, "d": 4}
        },
        "list1": {
            "status": "changed",
            "old_value": [1, 2, 3],
            "new_value": [4, 5, 6]
        }
    }
    
    assert parsed == expected


def test_json_output_format():
    """Тестирует формат вывода JSON (отступы и структура)."""
    diff = {
        "key": DiffNode(
            key="key",
            status=DiffStatus.ADDED,
            new_value="value"
        )
    }
    
    result = json_formatter(diff)
    
    assert result.startswith("{\n")
    assert result.endswith("\n}")
    assert '"status": "added"' in result
    assert '"value": "value"' in result
    
    parsed = json.loads(result)
    assert "key" in parsed
    assert parsed["key"]["status"] == "added"
    assert parsed["key"]["value"] == "value"
