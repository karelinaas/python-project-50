from gendiff.scripts.diff_builder import build_diff
from gendiff.formatters.formatter import json_formatter, plain, stylish


def generate_diff(
    first_data: dict,
    second_data: dict,
    format_name: str = "stylish",
) -> str:
    """
    Генерирует различия между двумя словарями и возвращает
    отформатированную строку.
    
    Args:
        first_data: Первый словарь для сравнения
        second_data: Второй словарь для сравнения
        format_name: Название форматера (по умолчанию "stylish")
        
    Returns:
        Отформатированная строка с различиями
    """
    # Строим внутреннее представление различий
    diff = build_diff(first_data, second_data)
    
    # Выбираем форматер и форматируем результат
    match format_name:
        case "stylish":
            return stylish(diff)
        case "plain":
            return plain(diff)
        case "json":
            return json_formatter(diff)
        case _:
            raise ValueError(f"Unsupported format: {format_name}")
