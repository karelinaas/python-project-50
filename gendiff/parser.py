import json
import yaml
from pathlib import Path


def parse_file(file_path: str) -> dict:
    """Парсинг файла в зависимости от его расширения."""
    path = Path(file_path)
    extension = path.suffix.lower()
    
    with open(file_path, "r") as f:
        if extension == ".json":
            return json.load(f)
        elif extension in (".yml", ".yaml"):
            return yaml.safe_load(f)
        else:
            raise ValueError(f"Unsupported file format: {extension}")
