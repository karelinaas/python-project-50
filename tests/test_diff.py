import json
import os
import tempfile

from gendiff import generate_diff


def test_generate_diff_added_key():
    """Тестирует diff, когда во втором файле добавлены ключи."""
    first_data = {"host": "hexlet.io", "timeout": 50}
    second_data = {"host": "hexlet.io", "timeout": 50, "verbose": True}
    
    result = generate_diff(first_data, second_data)
    expected = "{\n    host: hexlet.io\n    timeout: 50\n  + verbose: True\n}"
    
    assert result == expected


def test_generate_diff_removed_key():
    """Тестирует diff, когда из второго файла удалены ключи."""
    first_data = {"host": "hexlet.io", "timeout": 50, "verbose": True}
    second_data = {"host": "hexlet.io", "timeout": 50}
    
    result = generate_diff(first_data, second_data)
    expected = "{\n    host: hexlet.io\n    timeout: 50\n  - verbose: True\n}"
    
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
    expected = "{\n  - follow: False\n    host: hexlet.io\n  - proxy: 123.234.53.22\n  - timeout: 50\n  + timeout: 20\n  + verbose: True\n}"
    
    assert result == expected


def test_generate_diff_empty_files():
    """Тестирует diff с пустыми файлами."""
    first_data = {}
    second_data = {}
    
    result = generate_diff(first_data, second_data)
    expected = "{\n\n}"
    
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
        expected = "{\n    host: hexlet.io\n  - timeout: 50\n  + timeout: 20\n}"
        
        assert result == expected
