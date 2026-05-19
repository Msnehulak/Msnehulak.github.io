from datetime import datetime
import json
import os
import re

HTML_FOOTER = """<footer>
    <p>&copy; 2026 SnehulakTV_</p>
</footer>
"""

class Blog:
    def __init__(self):
        self.worker = Worker()
        self.json_blog_path = "data/blogs.json" 
        self.blog_path = "blogs.html"
        self.start = """
<!DOCTYPE html>
<html lang="cs">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SnehulakTV_'s site</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>

    <nav>
        <div class="logo">SnehulakTV_</div>
        <div class="odkazy">
            <a href="https://msnehulak.github.io/">Home</a>
            <a href="https://msnehulak.github.io/projects.html">Projects</a>
            <a href="https://msnehulak.github.io/blogs.html">blogs</a>
        </div>
    </nav>

    <header>
        <h1>My Blogs</h1>
    </header>
    <main>
"""

    def main(self):
        self.json_blog = self.worker.load_json(self.json_blog_path)
        self.update()
        self.worker.write_html(self.blog_path, self.blog)


    def update(self):
        blog = ""
        blog += self.start
        for i in self.json_blog:
            blog += f"""
        <section class="karta">
            <div class="hlavicka-blogu">
                <h2>{i["title"]}</h2>
                <span class="cas-blogu">{datetime.fromisoformat(i["time"]).strftime("%d.%m.%Y %H:%M")}</span>
            </div>
            <p>{i["content"]}</p> 
        </section>
        <br>
            """
            print(f"Blog {i['title']} was add.")
        blog += HTML_FOOTER
        blog += "</main></body></html>"

        self.blog = blog 

class Redirect:
    def __init__(self):
        self.worker = Worker()
        self.json_links_path = "data/links.json"
        self.links_folder = "r/"
        self.links = self.worker.load_json(self.json_links_path)
    @staticmethod
    def create_html(link, name):
        return f"""<!DOCTYPE HTML>
<html lang="cs">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="refresh" content="0; url={link}">
    <title>Přesměrování na {name}</title>
</head>
<body>
    <p>Pokud nebudete automaticky přesměrováni na '{name}', klikněte na <a href="{link}">tento odkaz</a>.</p>
</body>
</html>
"""
    def main(self):            
        for i in self.links:
            html = self.create_html(i["link"], i["name"])
            
            target_folder = os.path.join(self.links_folder, i["r"])
            
            if not os.path.exists(target_folder):
                os.makedirs(target_folder)

            path = os.path.join(target_folder, "index.html")
            self.worker.write_html(path, html)

            print(f"Redirect '{i['name']}' was created under clean URL: /r/{i['r']}/")

    def add_redirect(self, link="https://www.google.com", name = "Google", r="g"):
        links = self.links
        links.append({"link": link, "name": name, "r": r})
        self.worker.write_json("data/links.json", links)
        print(f"Link {name} ({link}) is add as '{r}'")

class Worker:
    def __init__(self) -> None:
        pass

    def set_up(self): 
        self.app_blog = Blog()
        self.app_redirect = Redirect()

    def blog_start(self):
        self.app_blog.main()

    def redirect_start(self):
        self.app_redirect.main()

    def redirect_add(self):
        ulink = input("link:")
        uname = input("Name:")
        ur = input("Redirect:")
        self.app_redirect.add_redirect(link=ulink, name=uname, r=ur)

    @staticmethod
    def load_json(path):
        with open(path, "r", encoding='utf-8') as f:
            return json.load(f)

    @staticmethod
    def write_json(path, data):
        with open(path, "w", encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    @staticmethod
    def write_html(path, content):
        with open(path, "w", encoding='utf-8') as file:
            file.write(content)

def clear_data(issue_body):
    data = {}
    sections = re.split(r'###\s+', issue_body)
   
    for section in sections:
        if not section.strip():
            continue
        lines = section.split('\n', 1)
        key = lines[0].strip().lower().replace(" ", "_")
        value = lines[1].strip() if len(lines) > 1 else ""

        data[key] = value.strip()
        
    return data

if __name__ == "__main__":
    app = Worker()
    app.set_up()
    
    if "ISSUE_BODY" in os.environ:
        print("Running in automated mode (GitHub Action)...")
        body = os.environ["ISSUE_BODY"]
        parsed_data = clear_data(body)
        
        link = parsed_data.get("web_link")
        name = parsed_data.get("name_of_redirect")
        r = parsed_data.get("redirect")
        
        if link and name and r:
            app.app_redirect.add_redirect(link=link, name=name, r=r)
            app.redirect_start()
            app.blog_start()
            print("SUCCESS: Automation finished successfully.")
        else:
            print("ERROR: Could not parse all required fields from Issue Body.")
            print(f"Parsed data: {parsed_data}")
            exit(1)

    else:
        while True:
            uinp = input("/Web.manager/").strip()
            if uinp.startswith("run"):
                if uinp.endswith("blog"):
                    app.blog_start()
                elif uinp.endswith("redirect") or uinp.endswith("re"):
                    app.redirect_start()
                elif uinp.endswith("all"):
                    app.redirect_start()
                    app.blog_start()
                else:
                    print("ERROR: I don't know what to run")
            elif uinp.startswith("add"):
                if uinp.endswith("redirect") or uinp.endswith("re"):
                    app.redirect_add()
