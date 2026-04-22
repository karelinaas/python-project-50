import json
import os
import tempfile
import yaml

from gendiff import generate_diff
from gendiff.parser import parse_file


def test_generate_diff_added_key():
    """Тестирует diff, когда во втором файле добавлены ключи."""
    first_data = {"host": "hexlet.io", "timeout": 50}
    second_data = {"host": "hexlet.io", "timeout": 50, "verbose": True}
    
    result = generate_diff(first_data, second_data)
    expected = "{\n    host: hexlet.io\n    timeout: 50\n  + verbose: true\n}"
    
    assert result == expected


def test_generate_diff_removed_key():
    """Тестирует diff, когда из второго файла удалены ключи."""
    first_data = {"host": "hexlet.io", "timeout": 50, "verbose": True}
    second_data = {"host": "hexlet.io", "timeout": 50}
    
    result = generate_diff(first_data, second_data)
    expected = "{\n    host: hexlet.io\n    timeout: 50\n  - verbose: true\n}"
    
    assert result == expected


def test_generate_diff_changed_value():
    """Тестирует diff, когда значения различаются."""
    first_data = {"host": "hexlet.io", "timeout": 50}
    second_data = {"host": "hexlet.io", "timeout": 20}
    
    result = generate_diff(first_data, second_data)
    expected = "{\n    host: hexlet.io\n  - timeout: 50\n  + timeout: 20\n}"
    
    assert result == expected


def test_generate_diff_complex():
    """Тестирует diff с множественными изменениями."""
    first_data = {
        "host": "hexlet.io",
        "timeout": 50,
        "proxy": "123.234.53.22",
        "follow": False
    }
    second_data = {
        "host": "hexlet.io",
        "timeout": 20,
        "verbose": True
    }
    
    result = generate_diff(first_data, second_data)
    expected = (
        "{\n  - follow: false\n    host: hexlet.io\n  - proxy: "
        "123.234.53.22\n  - timeout: 50\n  + timeout: 20\n  + verbose: true\n}"
    )
    
    assert result == expected


def test_generate_diff_empty_files():
    """Тестирует diff с пустыми файлами."""
    first_data = {}
    second_data = {}
    
    result = generate_diff(first_data, second_data)
    expected = "{\n}"
    
    assert result == expected


def test_generate_diff_first_empty():
    """Тестирует diff, когда первый файл пустой."""
    first_data = {}
    second_data = {"host": "hexlet.io"}
    
    result = generate_diff(first_data, second_data)
    expected = "{\n  + host: hexlet.io\n}"
    
    assert result == expected


def test_generate_diff_second_empty():
    """Тестирует diff, когда второй файл пустой."""
    first_data = {"host": "hexlet.io"}
    second_data = {}
    
    result = generate_diff(first_data, second_data)
    expected = "{\n  - host: hexlet.io\n}"
    
    assert result == expected


def test_generate_diff_with_files():
    """Тестирует diff с использованием реальных JSON файлов."""
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create first file
        file1_path = os.path.join(temp_dir, "file1.json")
        with open(file1_path, 'w') as f:
            json.dump({"host": "hexlet.io", "timeout": 50}, f)
        
        # Create second file
        file2_path = os.path.join(temp_dir, "file2.json")
        with open(file2_path, 'w') as f:
            json.dump({"host": "hexlet.io", "timeout": 20}, f)
        
        # Load files and compare
        with open(file1_path, 'r') as f:
            first_data = json.load(f)
        
        with open(file2_path, 'r') as f:
            second_data = json.load(f)
        
        result = generate_diff(first_data, second_data)
        expected = (
            "{\n    host: hexlet.io\n  - timeout: 50\n  + timeout: 20\n}"
        )
        
        assert result == expected


def test_parse_file_json():
    """Тестирует парсинг JSON файлов."""
    with tempfile.TemporaryDirectory() as temp_dir:
        file_path = os.path.join(temp_dir, "test.json")
        test_data = {"host": "hexlet.io", "timeout": 50}
        
        with open(file_path, 'w') as f:
            json.dump(test_data, f)
        
        result = parse_file(file_path)
        assert result == test_data


def test_parse_file_yaml():
    """Тестирует парсинг YAML файлов."""
    with tempfile.TemporaryDirectory() as temp_dir:
        file_path = os.path.join(temp_dir, "test.yml")
        test_data = {"host": "hexlet.io", "timeout": 50}
        
        with open(file_path, 'w') as f:
            yaml.dump(test_data, f)
        
        result = parse_file(file_path)
        assert result == test_data


def test_parse_file_yaml_extension():
    """Тестирует парсинг YAML файлов с расширением .yaml."""
    with tempfile.TemporaryDirectory() as temp_dir:
        file_path = os.path.join(temp_dir, "test.yaml")
        test_data = {"host": "hexlet.io", "timeout": 50}
        
        with open(file_path, 'w') as f:
            yaml.dump(test_data, f)
        
        result = parse_file(file_path)
        assert result == test_data


def test_parse_file_unsupported_format():
    """Тестирует исключение для неподдерживаемого формата."""
    with tempfile.TemporaryDirectory() as temp_dir:
        file_path = os.path.join(temp_dir, "test.txt")
        
        with open(file_path, 'w') as f:
            f.write("some text")
        
        try:
            parse_file(file_path)
            assert False, "Should raise ValueError"
        except ValueError as e:
            assert "Unsupported file format" in str(e)


def test_generate_diff_with_yaml_files():
    """Тестирует diff с использованием реальных YAML файлов."""
    with tempfile.TemporaryDirectory() as temp_dir:
        file1_path = os.path.join(temp_dir, "file1.yml")
        with open(file1_path, 'w') as f:
            yaml.dump({"host": "hexlet.io", "timeout": 50}, f)
        
        file2_path = os.path.join(temp_dir, "file2.yml")
        with open(file2_path, 'w') as f:
            yaml.dump({"host": "hexlet.io", "timeout": 20}, f)
        
        first_data = parse_file(file1_path)
        second_data = parse_file(file2_path)
        
        result = generate_diff(first_data, second_data)
        expected = (
            "{\n    host: hexlet.io\n  - timeout: 50\n  + timeout: 20\n}"
        )
        
        assert result == expected


def test_generate_diff_complex_yaml():
    """Тестирует сложный diff с YAML файлами как в примере."""
    with tempfile.TemporaryDirectory() as temp_dir:
        file1_path = os.path.join(temp_dir, "file1.yml")
        first_data = {
            "follow": False,
            "host": "hexlet.io",
            "proxy": "123.234.53.22",
            "timeout": 50
        }
        with open(file1_path, 'w') as f:
            yaml.dump(first_data, f)
        
        file2_path = os.path.join(temp_dir, "file2.yml")
        second_data = {
            "host": "hexlet.io",
            "timeout": 20,
            "verbose": True
        }
        with open(file2_path, 'w') as f:
            yaml.dump(second_data, f)
        
        first_parsed = parse_file(file1_path)
        second_parsed = parse_file(file2_path)
        
        result = generate_diff(first_parsed, second_parsed)
        expected = (
            "{\n  - follow: false\n    host: hexlet.io\n  "
            "- proxy: 123.234.53.22\n  "
            "- timeout: 50\n  + timeout: 20\n  + verbose: true\n}"
        )
        
        assert result == expected


def test_generate_diff_nested_structures():
    """Тестирует diff с вложенными структурами."""
    first_data = {
        "common": {
            "setting1": "Value 1",
            "setting2": 200,
            "setting3": True
        },
        "group1": {
            "baz": "bas"
        },
        "group2": {
            "foo": "bar"
        }
    }
    
    second_data = {
        "common": {
            "setting1": "Value 1",
            "setting3": False,
            "setting4": "new value"
        },
        "group1": {
            "foo": "bar",
            "baz": "bars"
        },
        "group3": {
            "foo": "baz"
        }
    }
    
    result = generate_diff(first_data, second_data)
    
    assert "group3" in result
    assert "foo: baz" in result
    assert "- setting2: 200" in result
    assert "+ setting4: new value" in result
    assert "- setting3: true" in result
    assert "+ setting3: false" in result


def test_generate_diff_deeply_nested():
    """Тестирует diff с глубоко вложенными структурами."""
    first_data = {
        "database": {
            "host": "localhost",
            "port": 5432,
            "credentials": {
                "username": "admin",
                "password": "secret"
            },
            "options": {
                "timeout": 30,
                "retry": 3
            }
        }
    }
    
    second_data = {
        "database": {
            "host": "remote-server",
            "port": 5432,
            "credentials": {
                "username": "admin",
                "password": "new-secret"
            },
            "options": {
                "timeout": 60,
                "ssl": True
            }
        }
    }
    
    result = generate_diff(first_data, second_data)
    
    assert "- host: localhost" in result
    assert "+ host: remote-server" in result
    assert "- password: secret" in result
    assert "+ password: new-secret" in result
    assert "- timeout: 30" in result
    assert "+ timeout: 60" in result
    assert "+ ssl: true" in result
    assert "- retry: 3" in result
