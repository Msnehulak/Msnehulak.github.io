from datetime import datetime, timedelta
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
BASE_TIME_FORM = "%Y-%m-%d %H:%M:%S"

CACHE_PATH = BASE_DIR / "cache"
DATA_PATH = BASE_DIR / "data"

CACHE_MASTER_PATH = CACHE_PATH / "master.json"

class Cache:
    def __init__(self):
        with open(CACHE_MASTER_PATH, "r") as f:
            self.master = json.load(f)
    
    def get(self, index):
        for x in self.master:
            if x.get("index") == index:
                # 1. Načtení dat
                try:
                    with open(CACHE_PATH / x["file"], "r") as f:
                        data = json.load(f)
                except FileNotFoundError:
                    return {"data": None, "meta": x, "update": True}


                last_update = datetime.strptime(x["last"], BASE_TIME_FORM)
                expiry_limit = last_update + timedelta(hours=x["frequency"])
                
                need_update = datetime.now() > expiry_limit
                
                return {"data": data, "meta": x, "update": need_update}
        
        return None
    
    def update(self, index, data=None):
        # 1. Najdeme správný záznam v listu
        for x in self.master:
            if x.get("index") == index:
                # 2. Převedeme datetime na string pomocí tvého formátu
                x['last'] = datetime.now().strftime(BASE_TIME_FORM)
                
                if data is not None:
                    try:
                        with open(CACHE_PATH / x["file"], "w") as f:
                            json.dump(data, f, indent=4, ensure_ascii=False)
                    except Exception as e:
                        print(f"Chyba při zápisu dat pro index '{index}': {e}")
                        return False
                
                # 4. Uložíme aktualizovaný master.json zpět na disk
                self._save_master()
                return True
        
        print(f"Index '{index}' nelze aktualizovat, chybí v master.json")
        return False

    def _save_master(self):
        with open(CACHE_MASTER_PATH, "w") as f:
            json.dump(self.master, f, indent=4, ensure_ascii=False)

cache = Cache()
