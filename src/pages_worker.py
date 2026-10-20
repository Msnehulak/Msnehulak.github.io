import os
from pathlib import Path

import frontmatter
import markdown
from dotenv import load_dotenv
from jinja2 import Environment, meta
from sqlmodel import Session, create_engine

from . import pages_db

load_dotenv()

site_url = os.getenv("SITEURL", "https://example.com").rstrip("/")
root_dir = Path(__file__).parent.parent.resolve()
content_dir = root_dir / "content"
output_dir = root_dir / "output"


class IndexContent:  # Opraveno: velká počáteční písmena (konvence pro třídy)
    def __init__(self) -> None:  # Opraveno: None s velkým N
        self.index_func = {".md": self.index_mark_down}
        self.db_engine = create_engine("sqlite:///ssg.db")
        self.jinja2_env = Environment()
        self.main()

    def main(self):
        content_list = []

        for i in content_dir.rglob("*"):
            if i.is_file():
                if i.suffix in self.index_func:
                    self.index_func[i.suffix](i)
                    content_list.append(i)

        print(content_list)

    def index_mark_down(self, path: Path):
        page = frontmatter.load(path)

        html_content = markdown.markdown(page.content)

        page_variables = self.jinja2_env.parse(html_content)
        page_dependencys = list(meta.find_undeclared_variables(page_variables))

        lang = page.metadata.get("lang", path.stem)
        slug = page.metadata.get("slug", path.stem)
        description = page.metadata.get("description", "No description")
        title = page.metadata.get("title", "No title")
        save_as = page.metadata.get("save_as", None)

        if lang == "en":
            path_lang = ""
        else:
            path_lang = f"{lang}/"

        if save_as == "index":
            page_path = f"{path_lang}"
        else:
            page_path = f"{path_lang}{slug}/"

        page_save_as = output_dir / page_path / "index.html"
        page_url = f"{site_url}/{page_path}"

        page_id = f"{lang}{slug}"

        page_row = pages_db.Page(
            id=page_id,
            slug=slug,
            content=html_content,
            lang=lang,
            title=title,
            description=description,
            dependencys=page_dependencys,
            url=page_url,
            save_as=str(page_save_as),
        )

        with Session(self.db_engine) as session:
            session.add(page_row)
            session.commit()
            print(f"Záznam '{slug}' úspěšně přidán!")


# Spuštění pro test:
if __name__ == "__main__":
    indexer = IndexContent()
    indexer.main()
