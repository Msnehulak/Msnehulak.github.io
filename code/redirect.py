import sys
import sweb
import webbuilder as wb
import os
from pathlib import Path

class Redirect:
    def __init__(self) -> None:
        self.links = sweb.load_json("links")
        self.texts = sweb.data.texts
        self.links_folder = sweb.BASE_DIR / "web" / "r"

    def create_html(self, link, name):
        bld = wb.WebBuilder(add_nav=False, add_start=False)
        bld.add_start(load_css=False, redirect=link, title=name)
        
        msg_cs = self.texts["cs"]["redirect"]["nl_msg"]
        click_cs = self.texts["cs"]["redirect"]["nl_click"]
        
        msg_en = self.texts["en"]["redirect"]["nl_msg"]
        click_en = self.texts["en"]["redirect"]["nl_click"]
        
        # Přidání obou hlášek pro uživatele pod sebe
        bld.add_markdown(f"{msg_en} [{click_en}]({link})")
        bld.add_markdown(f"{msg_cs} [{click_cs}]({link})")
       
        bld.build(add_footer=True)
        return bld.get_web()

    def main(self):            
        for i in self.links:
            html_content = self.create_html(i["link"], i["name"])
            
            target_folder = self.links_folder / i["r"]
            target_folder.mkdir(parents=True, exist_ok=True)

            path = target_folder / "index.html"
            with open(path, "w", encoding='utf-8') as f:
                f.write(html_content)

            print(f"Redirect '{i['name']}' at /r/{i['r']}/")

    def validate_redirect(self, name, link, r):
        limits = sweb.data.limits["redirect"]    
   
        def check(value, blocks, name="unknown"):
            if len(value) > blocks["len"]:
                print(f"{name} Lenght is over limit {blocks['len']}")
                sys.exit(1)
            for block in blocks["block"]:
                if block in value:
                    print(f"is use block world {block}. {blocks['block']}")
                    sys.exit(1)

        check(name, limits["name"], "name")
        check(link, limits["link"], "link")
        check(r, limits["r"], "redirect")

    def add_redirect(self, link="https://www.google.com", name="Google", r="g"):
        self.validate_redirect(name, link, r)
        
        for existing in self.links:
            if existing["r"] == r:
                print(f"Redirect with path '/r/{r}/' already exists")
                sys.exit(1)
        
        add = {"link": link, "name": name, "r": r}
        self.links.append(add)
        sweb.save_json("links", self.links)

if __name__ == "__main__":
    app = Redirect()
    app.main()
