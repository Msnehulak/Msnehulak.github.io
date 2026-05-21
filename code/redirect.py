import sweb
import webbuilder as wb
import os
from pathlib import Path

class Redirect:
    def __init__(self) -> None:
        self.links = sweb.load_json("links")
        self.text = sweb.data.texts["redirect"]
        self.links_folder = sweb.BASE_DIR / "web" / "r"

    def create_html(self, link, name):
        bld = wb.WebBuilder(add_nav=False, add_start=False)
        bld.add_start(load_css=False, redirect=link, title=name)
        msg = self.text["nl_msg"]["cs"]
        click = self.text["nl_click"]["cs"]
        bld.add_text(f"{msg} ::link({link}):{click}::link::")
        bld.build(add_footer=True)
        return bld.get_web()

    def main(self):            
        for i in self.links:
            html_content = self.create_html(i["link"], i["name"])
            
            target_folder = self.links_folder / i["r"]
            target_folder.mkdir(parents=True, exist_ok=True)

            # Uložení index.html do dané složky
            path = target_folder / "index.html"
            with open(path, "w", encoding='utf-8') as f:
                f.write(html_content)

            print(f"Redirect '{i['name']}' at /r/{i['r']}/")

    def add_redirect(self, 
                link="https://www.google.com", 
                name = "Google", r="g"):
        self.links.append({"link": link, "name": name, "r": r})
        sweb.save_json("links", self.links)
        print(f"Link {name} ({link}) is add as '{r}'")

if __name__ == "__main__":
    app = Redirect()
    app.main()
