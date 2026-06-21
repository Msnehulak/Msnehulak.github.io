import sweb
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
from ossapi import Ossapi

load_dotenv()
MINIMUM_UPDATE_HOURS = 1

class Osu:
    def __init__(self) -> None:
        self.name = "SnehulakTV_"
        self.data = sweb.load_json("cache/osu")

    def update_data(self, Force=False):
        last_update = datetime.strptime(self.data["update"], sweb.BASE_TIME_FORM)
        time_diff = datetime.now() - last_update 

        if time_diff < timedelta(hours=MINIMUM_UPDATE_HOURS) and not Force:
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
            self.data["country_rank"] = stats.country_rank 
            self.data["level"] = stats.level.current       
            self.data["avatar"] = user.avatar_url          
            self.data["ss_count"] = stats.grade_counts.ss 

            sweb.save_json("cache/osu", self.data)
            print("osu! cache was updated.")
        except Exception as e:
            print(f"ERROR with contact osu! API: {e}")

    def create_page(self, lang="en", prefix=""):
        def get_area(area):
            return f"{area[0]}x{area[1]}mm"

        texts = sweb.data.texts[lang]["osu"]

        total_seconds = int(self.data["play_time"])
        days = total_seconds // (24 * 3600)
        hours = (total_seconds % (24 * 3600)) // 3600
        minutes = (total_seconds % 3600) // 60
        play_time = f"{days}d  {hours}h {minutes}m"        

        i = texts["play_style"]
        head_profile = "Profil" if lang == "cs" else "Profile"
        head_style = "Herní styl" if lang == "cs" else "Play Style"
        
        # Čistý text stránky v Markdownu
        markdown_content = f"""# {head_profile}

![logo]({self.data["avatar"]}){{.osu-logo}}

- **Name:** {self.name}
- **Rank:** #{self.data["rank"]}
- **PP:** {self.data["pp"]}
- **Play Time:** {play_time}
- **Play Count:** {self.data["play_count"]}
- **ACC:** {self.data["acc"]:.2f}%

# {head_style}
**Pen grip:** {i["pen_grip"]}
**Area**: {get_area(i["area"])}
**Favorite Mods**: {", ".join(i["fav_mods"])}
"""

        # Front Matter hlavička pro Pelican, která definuje šablonu osu.html
        md_page = f"""Title: {texts["title"]}
Lang: {lang}
Slug: osu
Save_as: {prefix}osu.html
URL: {prefix}osu.html
Template: osu

{markdown_content}
"""
        
        target_dir = sweb.BASE_DIR / "content" / "pages" / prefix
        target_dir.mkdir(parents=True, exist_ok=True)
        
        with open(target_dir / "osu.md", "w", encoding="utf-8") as f:
            f.write(md_page)

    def main(self):
        self.update_data()
        self.create_page("en", "")
        self.create_page("cs", "cz/")

osu = Osu()

if __name__ == "__main__":
    osu.main()
