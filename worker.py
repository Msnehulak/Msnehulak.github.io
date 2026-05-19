from datetime import datetime
import json
import os
import re
import html

HTML_FOOTER = """<footer>
    <p>&copy; 2026 SnehulakTV_</p>
</footer>
"""

LIMITS = {
    "redirect": {
        "r": {
            "symbols": ["..", "/", "\\", " ", '"', "'", "&", "?", "#", "%", ";", "|", "<", ">", ":", "*"],
            "lenght": 50
        },
        "name": {
            "symbols": ["<", ">", "javascript:"],
            "lenght": 50
        },
        "link": {
            "symbols": ["<", ">", "javascript:", "\n", "\r", "`", "(", ")"],
            "lenght": 100 
        }
    }
}

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
                <span class="cas-blogu">{datetime.fromisoformat(i["time"].replace("Z", "+00:00")).strftime("%d.%m.%Y %H:%M")}</span>
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
        self.app_issue_worker = IssueWorker()

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

class IssueWorker():
    def __init__(self) -> None:
        self.worker = Worker()
        self.app_blog = Blog()
        self.app_redirect = Redirect()

    def validate_redirect(self, link, name, r):
            # Redirect
        r_limit = LIMITS["redirect"]["r"]
        for symbol in r_limit["symbols"]:
            if symbol in r.lower():
                print(f"ERROR: plese remove |{symbol}|. This is block symbol") 
                exit(1)
        if len(r) > r_limit["lenght"]:
            print(f"ERROR: redirect is over character limit of {r_limit['lenght']}")
            exit(1)
        r = html.escape(r)

            # Name
        name_limit = LIMITS["redirect"]["name"]
        for symbol in name_limit["symbols"]:
            if symbol in name.lower():
                print(f"ERROR: plese remove |{symbol}|. This is block symbol") 
                exit(1)
        if len(name) > name_limit["lenght"]:
            print(f"ERROR: name is over character limit of {name_limit['lenght']}")
            exit(1)
        name = html.escape(name)

            # Link
        https_check = not link.lower().startswith("https://")
        http_check = not link.lower().startswith("http://")
        if https_check and http_check:
            print("ERROR: pless use https or http link.")
            exit(1)
        link_limit = LIMITS["redirect"]["link"]
        for symbol in link_limit["symbols"]:
            if symbol in link.lower():
                print(f"ERROR: plese remove |{symbol}|. This is block symbol") 
                exit(1)
        if len(link) > link_limit["lenght"]:
            print(f"ERROR: web is over character limit of {link_limit['lenght']}")
            exit(1)
        link = html.escape(link)

    def clear_data(self):
        def find_type(data: str):
            counts = {
                "web_link": data.count("### Web link"),
                "redirect_name": data.count("### Name of redirect"),
                "redirect": data.count("### Redirect")
            }   
            web_link = counts["web_link"] == 1
            redirect_name = counts["redirect_name"] == 1 
            redirect = counts["redirect"] == 1

            if web_link and redirect_name and redirect:
                return "redirect"
            else:
                print("ERROR: Unknown issue form format!!")
                exit(1)
    
        def format_data(body: str):
            data = {}
            sections = re.split(r'###\s+', body)
            
            for section in sections:
                if not section.strip():
                    continue
                lines = section.split('\n', 1)
                key = lines[0].strip().lower().replace(" ", "_")
                value = lines[1].strip() if len(lines) > 1 else ""
                data[key] = value.strip()
            return data
       
        self.type = find_type(self.row_body)
        self.issue_body = format_data(self.row_body)

    def main(self):
        print("Running in automated mode (GitHub Action)...")
        self.row_body = os.environ["ISSUE_BODY"]
        self.clear_data()

        if self.type == "redirect":
            data = self.issue_body

            link = data.get("web_link")
            name = data.get("name_of_redirect")
            r = data.get("redirect")
            
            self.validate_redirect(link, name, r)

            name = html.escape(name)
            r = html.escape(r)

            if link and name and r:
                self.app_redirect.add_redirect(link=link, name=name, r=r)
                self.app_redirect.main()
                print("SUCCESS: Automation finished successfully.")
            else:
                print("ERROR: Could not parse all required fields from Issue Body.")
                print(f"Parsed data: {data}")
                exit(1)


if __name__ == "__main__":
    app = Worker()
    app.set_up()
    
    if "ISSUE_BODY" in os.environ:
        app.app_issue_worker.main()
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
