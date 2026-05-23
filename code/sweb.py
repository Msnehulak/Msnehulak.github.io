from datetime import datetime
from pathlib import Path
import json

BASE_DIR = Path(__file__).resolve().parent.parent
BASE_TIME_FORM = "%Y-%m-%d %H:%M:%S"

class Data:
    def __init__(self) -> None:
        self.copy_right_year = [2026, 2028]
        self.texts = load_json("text")
        self.limits = load_json("limits")

def log_error(text):
    error = f"ERROR[{datetime.now()}]: {text}"
    print(error)
    with open(BASE_DIR / "log.txt", "a", encoding="utf-8") as f:
        f.write(error)

def save_html(file: str, content: str):
    end = ".html"
    if not file.endswith(end):
        file += end
    
    path = BASE_DIR / "web" / file
    with open(path, "w", encoding='utf-8') as f:
        f.write(content)

def save_json(file: str, content):
    end = ".json"
    if not file.endswith(end):
        file += end

    content = json.dumps(content)
    path = BASE_DIR / "data" / file
    with open(path, "w", encoding='utf-8') as f:
        f.write(content)

def load_json(file: str):
    end = ".json"
    if not file.endswith(end):
        file += end

    path = BASE_DIR / "data" / file
    with open(path, "r", encoding='utf-8') as f:
        return json.load(f)

data = Data()
