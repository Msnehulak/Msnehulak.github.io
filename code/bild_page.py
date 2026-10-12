import frontmatter
import markdown
from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader("theme"))


def build_page(file_path):
    post = frontmatter.load(file_path)

    html_content = markdown.markdown(post.content)

    template = env.get_template("base.html")

    jija_values = {"page": post.metadata}

    output = template.render(content=html_content, **jija_values)

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(output)

    print("Všechna metadata byla úspěšně předána do šablony!")


if __name__ == "__main__":
    build_page("content/index/cs.md")
