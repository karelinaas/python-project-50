from typing import Dict, Any
from .diff_builder import DiffNode, DiffStatus


def format_stylish(diff: Dict[str, DiffNode], indent: int = 2) -> str:
    """
    Форматирует diff в стильный формат с отступами.
    
    Args:
        diff: Внутреннее представление различий
        indent: Базовый отступ
        
    Returns:
        Отформатированная строка с различиями
    """
    lines = ["{"]

    for key, node in diff.items():
        line = format_node(key, node, indent + 2)
        lines.append(line)
    
    lines.append("}")
    return "\n".join(lines)


def format_node(key: str, node: DiffNode, indent: int) -> str:
    """
    Форматирует отдельный узел diff.
    
    Args:
        key: Ключ узла
        node: Узел различий
        indent: Текущий отступ
        
    Returns:
        Отформатированная строка для узла
    """
    if node.status == DiffStatus.ADDED:
        return f"  + {key}: {format_value(node.new_value, indent)}"
    elif node.status == DiffStatus.REMOVED:
        return f"  - {key}: {format_value(node.old_value, indent)}"
    elif node.status == DiffStatus.CHANGED:
        lines = [
            f"  - {key}: {format_value(node.old_value, indent)}",
            f"  + {key}: {format_value(node.new_value, indent)}"
        ]
        return "\n".join(lines)
    elif node.status == DiffStatus.UNCHANGED:
        return f"    {key}: {format_value(node.old_value, indent)}"
    elif node.status == DiffStatus.NESTED:
        lines = [f"    {key}: {{"]
        for nested_key, nested_node in node.children.items():
            nested_line = format_node(nested_key, nested_node, indent + 4)
            lines.append(" " * (indent + 2) + nested_line)
        lines.append(" " * indent + "}")
        return "\n".join(lines)
    else:
        raise ValueError(f"Unknown status: {node.status}")


def format_value(value: Any, indent: int) -> str:
    """
    Форматирует значение для вывода.
    
    Args:
        value: Значение для форматирования
        indent: Текущий отступ
        
    Returns:
        Отформатированное значение
    """
    if value is None:
        return "null"
    elif isinstance(value, bool):
        return "True" if value else "False"
    elif isinstance(value, (int, float)):
        return str(value)
    elif isinstance(value, str):
        return value
    elif isinstance(value, dict):
        if not value:
            return "{}"
        lines = ["{"]
        for k, v in sorted(value.items()):
            formatted_val = format_value(v, indent + 2)
            lines.append(" " * (indent + 2) + f"{k}: {formatted_val}")
        lines.append(" " * indent + "}")
        return "\n".join(lines)
    elif isinstance(value, list):
        if not value:
            return "[]"
        lines = ["["]
        for item in value:
            formatted_item = format_value(item, indent + 2)
            lines.append(" " * (indent + 2) + formatted_item)
        lines.append(" " * indent + "]")
        return "\n".join(lines)
    else:
        return str(value)
