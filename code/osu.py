import sweb
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
from ossapi import Ossapi
import webbuilder as wb

load_dotenv()
MINIMUM_UPDATE_HOURS = 1

class Osu:
    def __init__(self) -> None:
        self.name = "SnehulakTV_"
        self.data = sweb.load_json("cache/osu")

    def update_data(self):
        last_update = datetime.strptime(self.data["update"], sweb.BASE_TIME_FORM)
        time_diff = datetime.now() - last_update 

        if time_diff < timedelta(hours=MINIMUM_UPDATE_HOURS):
            print("osu! data jsou aktuální (využívám cache).")
            return

        CLIENT_ID = os.getenv("OSU_CLIENT_ID")
        CLIENT_SECRET = os.getenv("OSU_CLIENT_SECRET")

        if not CLIENT_ID or not CLIENT_SECRET:
            print("Chyba: Chybí OSU_CLIENT_ID nebo OSU_CLIENT_SECRET. Přeskakuji update.")
            return

        try:
            api = Ossapi(int(CLIENT_ID), CLIENT_SECRET)
            user = api.user(self.name)
            stats = user.statistics

            self.data["update"] = datetime.now().strftime(sweb.BASE_TIME_FORM)
            self.data["pp"] = stats.pp
            self.data["acc"] = stats.hit_accuracy
            self.data["rank"] = stats.global_rank
            self.data["play_time"] = stats.play_time
            self.data["play_count"] = stats.play_count

            sweb.save_json("cache/osu", self.data)
            print("osu! cache was updated.")
        except Exception as e:
            print(f"ERROR with contntact osu! API: {e}")

    def get_stats(self):
        self.update_data()
        return self.data

    def create_page(self):
        def get_area(area):
            w = area[0]
            h = area[1]
            
            return f"{w}x{h}mm"
        texts = sweb.data.texts["osu"]

        bld = wb.WebBuilder(title=texts["title"])
        bld.add_head(text=texts["head"])

        frame = wb.Frame()
        i = texts["play_style"]
        
        content = f"""
# Stats

- **Name:** {self.name}
- **Rank:** {self.data["rank"]}
- **PP:** {self.data["pp"]}
- **Play Time:** {self.data["play_time"]}
- **Play Count:** {self.data["play_count"]}

# Play Style
**Pen grip:** {i["pen_grip"]} .nl.
**Area**: {get_area(i["area"])}

"""
        frame.add_markdown(content)
        frame.move_main()
        bld.add_html(frame.get_frame())

        bld.build()
        bld.save_web("osu")

    def main(self):
        self.update_data()
        self.create_page()

osu = Osu()
