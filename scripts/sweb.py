from datetime import datetime, timedelta
import json
import os
import yaml
import time
from pathlib import Path
from contextlib import contextmanager
from dotenv import load_dotenv

load_dotenv()

site_url = os.getenv('SITEURL', 'https://example.com').rstrip('/')
site_lan = 'en'

BASE_DIR = Path(__file__).resolve().parent.parent
BASE_TIME_FORM = "%Y-%m-%d %H:%M:%S"


LOAD_FOROM_DATA = [
    {'type': 'yaml', 'name': 'links', 'file': 'links'},
    {'type': 'yaml', 'name': 'osu', 'file': 'osu_stats'},
    {'type': 'yaml', 'name': 'projects', 'file': 'projects'},
    {'type': 'yaml', 'name': 'exlib', 'file': 'external_download'},
    {'type': 'yaml', 'name': 'games', 'file': 'games'},
    {'type': 'yaml', 'name': 'tran', 'file': 'translate'},
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

CREATE_PATHS = [

]

def create_paths():
    for path in CREATE_PATHS:
        path['path'].mkdir(parents=True, exist_ok=True)
        print(f">>> create path: {path['path']}")

def s_to_time(s: int = 0, m: int = 0, h: int = 0, d: int = 0, lan: str = 'en') -> str:
    seconds = s + m*60 + h*3600 + d*86400
    if seconds == 0:
        zero_labels = {'en': '0 seconds', 'cs': '0 sekund'}
        return zero_labels.get(lan, '0 s')

    d, dr = divmod(seconds, 86400)
    h, hr = divmod(dr, 3600)
    m, s = divmod(hr, 60)

    units = [
        (d, {'en': ('day', 'days'), 'cs': ('den', 'dny', 'dní'), 'fallback': 'D'}),
        (h, {'en': ('hour', 'hours'), 'cs': ('hodina', 'hodiny', 'hodin'), 'fallback': 'h'}),
        (m, {'en': ('minute', 'minutes'), 'cs': ('minuta', 'minuty', 'minut'), 'fallback': 'm'}),
        (s, {'en': ('second', 'seconds'), 'cs': ('sekunda', 'sekundy', 'sekund'), 'fallback': 's'}),
    ]

    def format_unit(value: int, translations: dict) -> str:
        if lan == 'cs':
            forms = translations['cs']
            if value == 1:
                unit = forms[0]
            elif 1 < value < 5:
                unit = forms[1]
            else:
                unit = forms[2]
        elif lan == 'en':
            forms = translations['en']
            unit = forms[0] if value == 1 else forms[1]
        else:
            unit = translations['fallback']
            
        return f'{value} {unit}'

    out = [format_unit(val, trans) for val, trans in units if val > 0]
    return ', '.join(out)
@contextmanager
def timer(name):
    start = time.perf_counter()
    yield
    elapsed = time.perf_counter() - start
    print(f"⏱️ [{name}] take {elapsed:.3f} s")
