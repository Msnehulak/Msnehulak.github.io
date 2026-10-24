from pathlib import Path

import markdown
from jinja2 import Environment, FileSystemLoader, select_autoescape
from sqlmodel import Session, create_engine, select

from . import pages_db

root_dir = Path(__file__).parent.parent.resolve()
theme_dir = root_dir / "theme"

MD_EXTENSIONS = ["extra", "fenced_code", "tables", "attr_list"]


class PagesBuilder:
    def __init__(self) -> None:
        self.db_engine = create_engine("sqlite:///ssg.db")
        self.theme_env = Environment(
            loader=FileSystemLoader(theme_dir),
            autoescape=select_autoescape(["html"]),
        )
        self.content_env = Environment(autoescape=False)

    def main(self):
        with Session(self.db_engine) as session:
            pages = session.exec(select(pages_db.Page)).all()

        for page in pages:
            self.build_page(page)

    def build_page(self, page: pages_db.Page):
        # jv = jinja variabls
        jv_global = {
            "page": {
                "title": page.title,
                "description": page.description,
                "url": page.url,
            }
        }
        jv_page = {
            **jv_global,
            "hello": "hi markdown",
        }
        jv_html = {
            **jv_global,
            "hello": "hello htlm",
        }
        ctx = {name: self.get_variable(name) for name in page.jija_dependencys}
        content_md = self.content_env.from_string(page.content).render(**jv_page)

        # 2) Markdown -> HTML
        content_html = markdown.markdown(content_md, extensions=MD_EXTENSIONS)

        # 3) Obalit theme/base.html
        template = self.theme_env.get_template("base.html")
        html = template.render(content=content_html, **jv_html)

        # 4) Zapsat na page.save_as (už obsahuje output/.../index.html)
        out_path = Path(page.save_as)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(html, encoding="utf-8")
        print(f"[OK] {page.url} -> {out_path}")

    def get_variable(self, name: str):
        # Sem napoj OSU_API, YOUTUBE_API, STEAM_API atd.
        # Zatím jen prázdný string, aby Jinja nespadla na Undefined.
        return ""
