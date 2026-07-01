import os
from pathlib import Path
from dotenv import load_dotenv
from ossapi import Ossapi
from diskcache import Cache

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
CACHE_DIR = BASE_DIR / "cache" / "diskcache"

class Osu:
    def __init__(self) -> None:
        self.data = None 
        self.cache = Cache(str(CACHE_DIR))
        self.update_frequency_hours = 1

    def load_data(self):
        cached_data = self.cache.get("osu") 
        
        if cached_data is None:
            print("Cache pro 'osu' neexistuje nebo vypršela. Spouštím update...")
            self._update()
            cached_data = self.cache.get("osu")

        if cached_data:
            self.data = cached_data
        else:
            print("Chyba: Nepodařilo se získat data z API ani z cache.")

    def _update(self):
        CLIENT_ID = os.getenv("OSU_CLIENT_ID")
        CLIENT_SECRET = os.getenv("OSU_CLIENT_SECRET")
        username = "SnehulakTV_"

        if not CLIENT_ID or not CLIENT_SECRET:
            print("Chyba: Chybí OSU_CLIENT_ID nebo OSU_CLIENT_SECRET v .env. Přeskakuji.")
            return

        try:
            api = Ossapi(int(CLIENT_ID), CLIENT_SECRET)
            user = api.user(username)
            stats = user.statistics

            novy_api_vystup = {
                "rank": stats.global_rank,
                "pp": stats.pp,
                "acc": stats.hit_accuracy,
                "play_time": stats.play_time,
                "play_count": stats.play_count,
                "avatar": user.avatar_url
            } 
            
            # Zápis do cache s nastavenou expirací (převod hodin na sekundy)
            expire_seconds = self.update_frequency_hours * 3600
            self.cache.set("osu", novy_api_vystup, expire=expire_seconds)
            
            print("osu! cache byla úspěšně aktualizována pomocí diskcache.")
            
        except Exception as e:
            print(f"Chyba při komunikaci s osu! API: {e}")

if __name__ == "__main__":
    app = Osu()
    app.load_data()
