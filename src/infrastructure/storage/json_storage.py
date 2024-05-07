import json
import os
from typing import Dict, Optional


class JsonStorage:
    """
    Provides functionality to store and retrieve JSON data for user sessions.
    """
    def __init__(self, storage_dir: str):
        self.storage_dir = storage_dir
        if not os.path.exists(storage_dir):
            os.makedirs(storage_dir)

    def save_data(self, file_name: str, data: Dict):
        """
        Saves data to a JSON file.
        Args:
            file_name (str): The name of the file to save the data in.
            data (Dict): The data to save.
        """
        file_path = os.path.join(self.storage_dir, f"{file_name}.json")
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    def load_data(self, file_name: str) -> Optional[Dict]:
        """
        Loads data from a JSON file.
        Args:
            file_name (str): The name of the file to load the data from.
        Returns:
            Optional[Dict]: The loaded data or None if the file does not exist.
        """
        file_path = os.path.join(self.storage_dir, f"{file_name}.json")
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as file:
                return json.load(file)
        return None
