from datetime import datetime
import json
import os


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
        self.links = self.worker.load_json(self.json_links_path)
            
        for i in self.links:
            html = self.create_html(i["link"], i["name"])
            
            target_folder = os.path.join(self.links_folder, i["r"])
            
            if not os.path.exists(target_folder):
                os.makedirs(target_folder)

            path = os.path.join(target_folder, "index.html")
            self.worker.write_html(path, html)

            print(f"Redirect '{i['name']}' was created under clean URL: /r/{i['r']}/")

class Worker:
    def __init__(self) -> None:
        pass

    def set_up(self): 
        self.app_blog = Blog()
        self.app_redirect = Redirect()

    def start_blog(self):
        self.app_blog.main()

    def start_redirect(self):
        self.app_redirect.main()

    @staticmethod
    def load_json(path):
        with open(path, "r", encoding='utf-8') as f:
            return json.load(f)

    @staticmethod
    def write_html(path, content):
        with open(path, "w", encoding='utf-8') as file:
            file.write(content)

if __name__ == "__main__":
    app = Worker()
    app.set_up()

    while True:
        uinp = input("/Web.manager/").strip()
        if uinp.startswith("run"):
            if uinp.endswith("blog"):
                app.start_blog()
            elif uinp.endswith("redirect") or uinp.endswith("re"):
                app.start_redirect()
            elif uinp.endswith("all"):
                app.start_redirect()
                app.start_blog()
            else:
                print("ERROR: I don't know what to run")

