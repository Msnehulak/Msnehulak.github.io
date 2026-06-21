import sys
import sweb
from pathlib import Path

class Redirect:
    def __init__(self) -> None:
        self.links = sweb.load_json("links")
        self.texts = sweb.data.texts

    def main(self):            
        content_redirect_folder = sweb.BASE_DIR / "content" / "r"
        content_redirect_folder.mkdir(parents=True, exist_ok=True)

        for i in self.links:
            msg_cs = self.texts["cs"]["redirect"]["nl_msg"]
            click_cs = self.texts["cs"]["redirect"]["nl_click"]
            
            msg_en = self.texts["en"]["redirect"]["nl_msg"]
            click_en = self.texts["en"]["redirect"]["nl_click"]

            md_redirect = f"""Title: Redirect {i['name']}
Save_as: r/{i['r']}/index.html
URL: r/{i['r']}/

<meta http-equiv="refresh" content="0; url={i['link']}">
<p>{msg_en} <a href="{i['link']}">{click_en}</a>.</p>
<p>{msg_cs} <a href="{i['link']}">{click_cs}</a>.</p>
"""
            path = content_redirect_folder / f"{i['r']}.md"
            with open(path, "w", encoding='utf-8') as f:
                f.write(md_redirect)

            print(f"Prepared redirect '{i['name']}' for /r/{i['r']}/")

    def validate_redirect(self, name, link, r):
        limits = sweb.data.limits["redirect"]    
  
        def check(value, blocks, name="unknown"):
            if len(value) > blocks["len"]:
                print(f"{name} Length is over limit {blocks['len']}")
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
