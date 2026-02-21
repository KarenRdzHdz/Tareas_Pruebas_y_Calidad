"""File manager module to handle JSON persistence."""

import json
from typing import Any, List


class FileManager:
    """Handles file read and write operations."""

    @staticmethod
    def load_data(file_path: str) -> List[Any]:
        """Load JSON data safely."""
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                return json.load(file)
        except FileNotFoundError:
            print(f"Error: {file_path} not found. Creating new file.")
            return []
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON format in {file_path}.")
            return []

    @staticmethod
    def save_data(file_path: str, data: List[Any]) -> None:
        """Save data to JSON file."""
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)
