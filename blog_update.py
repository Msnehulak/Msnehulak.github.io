import json

class UpdateBlog:
    def __init__(self) -> None:
        self.load_json()

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
            <a href="https://msnehulak.github.io/Snehulak.tv/">Home</a>
            <a href="https://msnehulak.github.io/Snehulak.tv/blogs.html">Projects</a>
            <a href="https://msnehulak.github.io/Snehulak.tv/blogs.html">blogs</a>
        </div>
    </nav>

    <header>
        <h1>My Blogs</h1>
    </header>
"""

    def load_json(self):
        with open("blogs.json", "r", encoding='utf-8') as f:
            self.json_blog = json.load(f)

    def update(self):
        blog = ""
        blog += self.start
        for i in self.json_blog:
            blog += f"""
    <main>
        <section class="karta">
            <h2>{i["title"]}</h2>
            <p>{i["content"]}</p> 
        </section>
    </main>
"""
        blog += "</body>"

        self.write_html(blog)

        print(blog)
    
    @staticmethod
    def write_html(blog):
        with open("blogs.html", "w") as file:
            file.write(blog)


    def main(self):
        print(self.json_blog)
        self.update()

if __name__ == "__main__":
    app = UpdateBlog()
    app.main()
