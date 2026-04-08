from typing import Dict, Any, List
from .diff_builder import DiffNode, DiffStatus


def stylish(diff: Dict[str, DiffNode]) -> str:
    """
    Форматирует diff в стильный формат с отступами.
    
    Args:
        diff: Внутреннее представление различий
        
    Returns:
        Отформатированная строка с различиями
    """
    lines = ["{"]
    lines.extend(_format_diff_nodes(diff, 4))
    lines.append("}")
    return "\n".join(lines)


def _format_diff_nodes(diff: Dict[str, DiffNode], indent: int) -> List[str]:
    """
    Рекурсивно форматирует узлы diff.
    
    Args:
        diff: Словарь с узлами различий
        indent: Текущий отступ
        
    Returns:
        Список отформатированных строк
    """
    lines = []
    sorted_keys = sorted(diff.keys())
    
    for key in sorted_keys:
        node = diff[key]
        lines.extend(_format_node(key, node, indent))
    
    return lines


def _format_node(key: str, node: DiffNode, indent: int) -> List[str]:
    """
    Форматирует отдельный узел diff.
    
    Args:
        key: Ключ узла
        node: Узел различий
        indent: Текущий отступ
        
    Returns:
        Список отформатированных строк
    """
    if node.status == DiffStatus.ADDED:
        return [f"{' ' * (indent - 2)}+ {key}: {_format_value(node.new_value, indent)}"]
    elif node.status == DiffStatus.REMOVED:
        return [f"{' ' * (indent - 2)}- {key}: {_format_value(node.old_value, indent)}"]
    elif node.status == DiffStatus.CHANGED:
        return [
            f"{' ' * (indent - 2)}- {key}: {_format_value(node.old_value, indent)}",
            f"{' ' * (indent - 2)}+ {key}: {_format_value(node.new_value, indent)}"
        ]
    elif node.status == DiffStatus.UNCHANGED:
        return [f"{' ' * indent}{key}: {_format_value(node.old_value, indent)}"]
    elif node.status == DiffStatus.NESTED:
        lines = [f"{' ' * indent}{key}: {{"]
        lines.extend(_format_diff_nodes(node.children, indent + 4))
        lines.append(f"{' ' * indent}}}")
        return lines
    else:
        raise ValueError(f"Unknown status: {node.status}")


def _format_value(value: Any, indent: int) -> str:
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
        return "true" if value else "false"
    elif isinstance(value, (int, float)):
        return str(value)
    elif isinstance(value, str):
        return value
    elif isinstance(value, dict):
        if not value:
            return "{}"
        lines = ["{"]
        for k, v in sorted(value.items()):
            formatted_val = _format_value(v, indent + 4)
            lines.append(f"{' ' * (indent + 4)}{k}: {formatted_val}")
        lines.append(f"{' ' * indent}}}")
        return "\n".join(lines)
    elif isinstance(value, list):
        if not value:
            return "[]"
        lines = ["["]
        for item in value:
            formatted_item = _format_value(item, indent + 4)
            lines.append(f"{' ' * (indent + 4)}{formatted_item}")
        lines.append(f"{' ' * indent}]")
        return "\n".join(lines)
    else:
        return str(value)
