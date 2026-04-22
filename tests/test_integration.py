"""Интеграционные тесты с использованием реальных тестовых файлов."""

import json
import os
from pathlib import Path

from gendiff import generate_diff
from gendiff.scripts.parser import parse_file


# Получаем путь к директории с тестовыми данными
TEST_DATA_DIR = Path(__file__).parent / "test_data"


def test_diff_with_simple_json_files():
    """Тестирует diff с использованием простых JSON файлов."""
    file1_path = TEST_DATA_DIR / "file1.json"
    file2_path = TEST_DATA_DIR / "file2.json"
    
    first_data = parse_file(str(file1_path))
    second_data = parse_file(str(file2_path))
    
    result = generate_diff(first_data, second_data)
    
    # Проверяем основные изменения
    assert "host: hexlet.io" in result
    assert "- timeout: 50" in result
    assert "+ timeout: 20" in result
    assert "- proxy: 123.234.53.22" in result
    assert "- follow: false" in result
    assert "+ verbose: true" in result


def test_diff_with_simple_yaml_files():
    """Тестирует diff с использованием простых YAML файлов."""
    file1_path = TEST_DATA_DIR / "file1.yml"
    file2_path = TEST_DATA_DIR / "file2.yml"
    
    first_data = parse_file(str(file1_path))
    second_data = parse_file(str(file2_path))
    
    result = generate_diff(first_data, second_data)
    
    # Проверяем основные изменения
    assert "host: hexlet.io" in result
    assert "- timeout: 50" in result
    assert "+ timeout: 20" in result
    assert "- proxy: 123.234.53.22" in result
    assert "- follow: false" in result
    assert "+ verbose: true" in result


def test_diff_with_complex_json_files():
    """Тестирует diff с использованием сложных JSON файлов с вложенными структурами."""
    file1_path = TEST_DATA_DIR / "filepath1.json"
    file2_path = TEST_DATA_DIR / "filepath2.json"
    
    first_data = parse_file(str(file1_path))
    second_data = parse_file(str(file2_path))
    
    result = generate_diff(first_data, second_data)
    
    # Проверяем изменения в секции common
    assert "common:" in result
    assert "setting1: Value 1" in result
    assert "- setting2: 200" in result
    assert "- setting3: true" in result
    assert "+ setting3: null" in result
    assert "+ setting4: blah blah" in result
    assert "+ setting5:" in result
    assert "+ follow: false" in result
    
    # Проверяем изменения в секции group1
    assert "group1:" in result
    assert "- baz: bas" in result
    assert "+ baz: bars" in result
    assert "foo: bar" in result
    assert "- nest:" in result
    assert "+ nest: str" in result
    
    # Проверяем изменения в секции group2/group3
    assert "- group2:" in result
    assert "+ group3:" in result
    assert "+ fee: 100500" in result
    
    # Проверяем глубокие вложения
    assert "- abc: 12345" in result
    assert "- deep:" in result
    assert "- id: 45" in result
    assert "+ deep:" in result
    assert "+ id:" in result
    assert "+ number: 45" in result
    
    # Проверяем изменения в setting6.doge
    assert "- wow: \"\"" in result
    assert "+ wow: so much" in result
    assert "+ ops: vops" in result


def test_parse_all_test_files():
    """Тестирует, что все тестовые файлы могут быть успешно распарсены."""
    test_files = [
        "file1.json",
        "file2.json", 
        "file1.yml",
        "file2.yml",
        "filepath1.json",
        "filepath2.json"
    ]
    
    for filename in test_files:
        file_path = TEST_DATA_DIR / filename
        assert file_path.exists(), f"Файл {filename} не существует"
        
        # Проверяем, что файл можно распарсить без ошибок
        data = parse_file(str(file_path))
        assert isinstance(data, dict), f"Файл {filename} должен содержать словарь"
        assert len(data) > 0, f"Файл {filename} не должен быть пустым"


def test_diff_consistency_between_json_and_yaml():
    """Проверяет, что diff для JSON и YAML версий одинаковых данных дает одинаковый результат."""
    # Простые файлы
    json_file1 = TEST_DATA_DIR / "file1.json"
    json_file2 = TEST_DATA_DIR / "file2.json"
    yaml_file1 = TEST_DATA_DIR / "file1.yml"
    yaml_file2 = TEST_DATA_DIR / "file2.yml"
    
    json_data1 = parse_file(str(json_file1))
    json_data2 = parse_file(str(json_file2))
    yaml_data1 = parse_file(str(yaml_file1))
    yaml_data2 = parse_file(str(yaml_file2))
    
    json_result = generate_diff(json_data1, json_data2)
    yaml_result = generate_diff(yaml_data1, yaml_data2)
    
    # Результаты должны быть идентичны
    assert json_result == yaml_result


def test_file_paths_existence():
    """Проверяет существование всех путей к тестовым файлам."""
    expected_files = [
        "file1.json",
        "file2.json",
        "file1.yml", 
        "file2.yml",
        "filepath1.json",
        "filepath2.json"
    ]
    
    for filename in expected_files:
        file_path = TEST_DATA_DIR / filename
        assert file_path.is_file(), f"Файл {file_path} не существует или не является файлом"
        assert file_path.stat().st_size > 0, f"Файл {file_path} пустой"


def test_complex_diff_structure():
    """Тестирует структуру сложного diff для проверки форматирования."""
    file1_path = TEST_DATA_DIR / "filepath1.json"
    file2_path = TEST_DATA_DIR / "filepath2.json"
    
    first_data = parse_file(str(file1_path))
    second_data = parse_file(str(file2_path))
    
    result = generate_diff(first_data, second_data)
    
    # Проверяем общую структуру вывода
    assert result.startswith("{")
    assert result.endswith("}")
    
    # Проверяем наличие правильных отступов и маркеров
    lines = result.split('\n')
    
    # Должны быть строки с добавленными и удаленными элементами
    added_lines = [line for line in lines if line.strip().startswith('+')]
    removed_lines = [line for line in lines if line.strip().startswith('-')]
    unchanged_lines = [line for line in lines if not line.strip().startswith(('+', '-')) and ':' in line]
    
    assert len(added_lines) > 0, "Должны быть добавленные элементы"
    assert len(removed_lines) > 0, "Должны быть удаленные элементы"
    assert len(unchanged_lines) > 0, "Должны быть неизмененные элементы"
