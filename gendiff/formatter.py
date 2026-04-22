import json
from typing import Any

from .diff_builder import DiffNode, DiffStatus


def stylish(diff: dict[str, DiffNode]) -> str:
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


def plain(diff: dict[str, DiffNode]) -> str:
    """
    Форматирует diff в plain формат с путями свойств.

    Args:
        diff: Внутреннее представление различий

    Returns:
        Отформатированная строка с различиями
    """
    lines = []
    _format_plain_nodes(diff, "", lines)
    return "\n".join(lines)


def json_formatter(diff: dict[str, DiffNode]) -> str:
    """
    Форматирует diff в структурированный JSON формат.

    Args:
        diff: Внутреннее представление различий

    Returns:
        Отформатированная JSON строка с различиями
    """
    result = {}
    sorted_keys = sorted(diff.keys())

    for key in sorted_keys:
        node = diff[key]
        result[key] = _format_node_for_json(node)

    return json.dumps(result, indent=2)


def _format_diff_nodes(diff: dict[str, DiffNode], indent: int) -> list[str]:
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


def _format_node(key: str, node: DiffNode, indent: int) -> list[str]:
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
        return [
            f"{' ' * (indent - 2)}+ {key}: "
            f"{_format_value(node.new_value, indent)}"
        ]
    elif node.status == DiffStatus.REMOVED:
        return [
            f"{' ' * (indent - 2)}- {key}: "
            f"{_format_value(node.old_value, indent)}"
        ]
    elif node.status == DiffStatus.CHANGED:
        return [
            f"{' ' * (indent - 2)}- {key}: "
            f"{_format_value(node.old_value, indent)}",
            f"{' ' * (indent - 2)}+ {key}: "
            f"{_format_value(node.new_value, indent)}"
        ]
    elif node.status == DiffStatus.UNCHANGED:
        return [
            f"{' ' * indent}{key}: {_format_value(node.old_value, indent)}"
        ]
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


def _format_plain_nodes(
    diff: dict[str, DiffNode],
    path: str, lines: list[str],
) -> None:
    """
    Рекурсивно форматирует узлы diff в plain формате.

    Args:
        diff: Словарь с узлами различий
        path: Текущий путь к свойству
        lines: Список для накопления строк
    """
    sorted_keys = sorted(diff.keys())

    for key in sorted_keys:
        node = diff[key]
        current_path = f"{path}.{key}" if path else key

        if node.status == DiffStatus.ADDED:
            if isinstance(node.new_value, (dict, list)):
                value_desc = "[complex value]"
            else:
                value_desc = _format_plain_value(node.new_value)
            lines.append(
                f"Property '{current_path}' was added with value: {value_desc}"
            )
        elif node.status == DiffStatus.REMOVED:
            lines.append(f"Property '{current_path}' was removed")
        elif node.status == DiffStatus.CHANGED:
            old_desc = _format_plain_value(node.old_value)
            new_desc = _format_plain_value(node.new_value)
            lines.append(
                f"Property '{current_path}' was updated. "
                f"From {old_desc} to {new_desc}"
            )
        elif node.status == DiffStatus.NESTED:
            _format_plain_nodes(node.children, current_path, lines)


def _format_plain_value(value: Any) -> str:
    """
    Форматирует значение для plain вывода.

    Args:
        value: Значение для форматирования

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
        return f"'{value}'"
    elif isinstance(value, (dict, list)):
        return "[complex value]"
    else:
        return str(value)


def _format_node_for_json(node: DiffNode) -> dict[str, Any]:
    """
    Форматирует узел diff для JSON вывода.

    Args:
        node: Узел различий

    Returns:
        Словарь с информацией об узле в формате JSON
    """
    result = {
        "status": node.status.value
    }
    
    if node.status == DiffStatus.ADDED:
        result["value"] = node.new_value
    elif node.status == DiffStatus.REMOVED:
        result["value"] = node.old_value
    elif node.status == DiffStatus.CHANGED:
        result["old_value"] = node.old_value
        result["new_value"] = node.new_value
    elif node.status == DiffStatus.UNCHANGED:
        result["value"] = node.old_value
    elif node.status == DiffStatus.NESTED:
        children = {}
        sorted_keys = sorted(node.children.keys())
        for key in sorted_keys:
            children[key] = _format_node_for_json(node.children[key])
        result["children"] = children
    
    return result
