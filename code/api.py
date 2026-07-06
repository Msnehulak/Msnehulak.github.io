import os
from pathlib import Path
from dotenv import load_dotenv
from ossapi import Ossapi
from diskcache import Cache

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
CACHE_DIR = BASE_DIR / "cache" / "diskcache"

ENV_VAL = {
    "osu_client_id": os.getenv("OSU_CLIENT_ID"),
    "osu_client_secret": os.getenv("OSU_CLIENT_SECRET"),
    "github_token": os.getenv("GIT_HUB_TOKEN")
}

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
        client_id = ENV_VAL['osu_client_id']
        client_secret = ENV_VAL['osu_client_secret']
        username = "SnehulakTV_"

        if not client_id or not client_secret:
            print("Chyba: Chybí OSU_client_id nebo OSU_CLIENT_SECRET v .env. Přeskakuji.")
            return

        try:
            api = Ossapi(int(client_id), client_secret)
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

class GitHub:
    def __init__(self) -> None:
        pass

if __name__ == "__main__":
    app = Osu()
    app.load_data()
