import json
from enum import Enum
from pathlib import Path
from typing import Any

import yaml


class DiffStatus(Enum):
    """Статусы изменений для ключа."""
    UNCHANGED = "unchanged"
    ADDED = "added"
    REMOVED = "removed"
    CHANGED = "changed"
    NESTED = "nested"


class DiffNode:
    """Узел в дереве различий."""
    
    def __init__(
        self,
        key: str,
        status: DiffStatus,
        old_value: Any = None,
        new_value: Any = None,
        children: dict[str, 'DiffNode'] = None
    ):
        self.key = key
        self.status = status
        self.old_value = old_value
        self.new_value = new_value
        self.children = children or {}
    
    def __repr__(self):
        return f"DiffNode(key={self.key}, status={self.status}, old_value={self.old_value}, new_value={self.new_value})"


def _parse_file_if_needed(data: dict[str, Any] | str) -> dict[str, Any]:
    if isinstance(data, str):
        if data.endswith(".json") or data.endswith(".yaml") or data.endswith(".yml"):
            path = Path(data)
            extension = path.suffix.lower()
            with open(Path(data), "r") as f:
                if extension == ".json":
                    return json.load(f)
                elif extension in (".yml", ".yaml"):
                    return yaml.safe_load(f)
        else:
            return json.load(data)
    return data


def build_diff(first_data: dict[str, Any] | str, second_data: dict[str, Any] | str) -> dict[str, DiffNode]:
    """
    Строит внутреннее представление различий между двумя словарями.
    
    Args:
        first_data: Первый словарь для сравнения
        second_data: Второй словарь для сравнения
        
    Returns:
        Словарь с узлами различий для каждого ключа
    """
    first_data = _parse_file_if_needed(first_data)
    second_data = _parse_file_if_needed(second_data)

    all_keys = sorted(set(first_data.keys()) | set(second_data.keys()))
    diff_result = {}
    
    for key in all_keys:
        if key in first_data and key not in second_data:
            diff_result[key] = DiffNode(
                key=key,
                status=DiffStatus.REMOVED,
                old_value=first_data[key]
            )
        elif key not in first_data and key in second_data:
            diff_result[key] = DiffNode(
                key=key,
                status=DiffStatus.ADDED,
                new_value=second_data[key]
            )
        elif key in first_data and key in second_data:
            old_val = first_data[key]
            new_val = second_data[key]
            
            if isinstance(old_val, dict) and isinstance(new_val, dict):
                nested_diff = build_diff(old_val, new_val)
                diff_result[key] = DiffNode(
                    key=key,
                    status=DiffStatus.NESTED,
                    children=nested_diff
                )
            elif old_val == new_val:
                diff_result[key] = DiffNode(
                    key=key,
                    status=DiffStatus.UNCHANGED,
                    old_value=old_val,
                    new_value=new_val
                )
            else:
                diff_result[key] = DiffNode(
                    key=key,
                    status=DiffStatus.CHANGED,
                    old_value=old_val,
                    new_value=new_val
                )
    
    return diff_result
