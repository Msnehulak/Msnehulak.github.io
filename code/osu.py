import os
from dotenv import load_dotenv
from ossapi import Ossapi
from . import sweb

class Osu:
    def __init__(self) -> None:
        self.data = None 

    def load_data(self):
        row_data = sweb.cache.get("osu") 
        
        if row_data is None:
            print("Index 'osu' nebyl v cache nalezen vůbec.")
            return
        self.data = row_data['data']

        if row_data["update"] == True: 
            self._update() 

    def _update(self):
        """
        Načtení reálných dat hráče z osu! API a update nové cache.
        """
        print("Cache vypršela. Stahuji nová data z osu! API...")
        
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

            # Příprava čistého slovníku s daty
            novy_api_vystup = {
                "rank": stats.global_rank,
                "pp": stats.pp,
                "acc": stats.hit_accuracy,
                "play_time": stats.play_time,
                "play_count": stats.play_count,
                "avatar": user.avatar_url
            } 
            
            # sweb.cache.update se postará o zápis do osu.json i aktualizaci času v master.json
            uspech = sweb.cache.update("osu", novy_api_vystup)
            if uspech:
                self.data = novy_api_vystup
                print("osu! cache byla úspěšně aktualizována v novém systému.")
        except Exception as e:
            print(f"Chyba při komunikaci s osu! API: {e}")

if __name__ == "__main__":
    app = Osu()
    app.load_data()
