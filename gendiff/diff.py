from .diff_builder import build_diff
from .formatter import format_stylish


def generate_diff(first_data: dict, second_data: dict) -> str:
    """
    Генерирует различия между двумя словарями и возвращает отформатированную строку.
    
    Args:
        first_data: Первый словарь для сравнения
        second_data: Второй словарь для сравнения
        
    Returns:
        Отформатированная строка с различиями
    """
    # Строим внутреннее представление различий
    diff = build_diff(first_data, second_data)
    
    # Форматируем результат
    return format_stylish(diff)
