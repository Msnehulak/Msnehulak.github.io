from datetime import datetime, timedelta
import json
import yaml
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
BASE_TIME_FORM = "%Y-%m-%d %H:%M:%S"

LOAD_FOROM_DATA = [
    {'type': 'yaml', 'name': 'links', 'file': 'links'},
    {'type': 'yaml', 'name': 'osu', 'file': 'osu_stats'},
    {'type': 'yaml', 'name': 'projects', 'file': 'projects'},
    {'type': 'yaml', 'name': 'exlib', 'file': 'external_download'},
]

class DataFolder:
    def __init__(self) -> None:
        self.data = {}
        self.data_path = BASE_DIR / 'data'
        self._save_loop()

    def _save_loop(self):
        for i in LOAD_FOROM_DATA:
            filetype = i['type']
            name = i['name']
            file = i['file']
            # Load data
            if filetype.lower() == 'yaml':
                path = self.data_path / f'{file}.yaml'
                content = self._load_yaml(path)
            elif filetype.lower() == 'json':
                path = self.data_path / f'{file}.json'
                content = self._load_json(path)
            else:
                print(f'unsuported format `{filetype}`')
                break
 
            if not content:
                print(f"file `{file}` is empty")

            self.data[name] = content

    @staticmethod
    def _load_yaml(file):
        try:
            with open(file, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except Exception as e:
            print(f"Error loading YAML {file}: {e}")
            return None

    @staticmethod
    def _load_json(file):
        try:
            with open(file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading JSON {file}: {e}")
            return None

_app_data_folder = DataFolder()
data = _app_data_folder.data

