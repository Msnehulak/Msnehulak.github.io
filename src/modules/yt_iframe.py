from pathlib import Path

import yaml
from jinja2 import Environment, FileSystemLoader, select_autoescape

root_dir = Path(__file__).parent.parent.parent.resolve()
theme_dir = root_dir / "theme"

VALID_STYLES = {"full", "icon", "text", "pill", "profile"}

_links_env = Environment(
    loader=FileSystemLoader(theme_dir),
    autoescape=select_autoescape(["html", "xml"]),
    trim_blocks=True,
    lstrip_blocks=True,
)


def download_thumbnail(yt_id: str):
    url = f"https://i.ytimg.com/vi/{yt_id}/hqdefault.jpg"

    return url


def yt_iframe(yt_id: str, lang: str = "en", style: str = "full") -> str:
    """Vrátí HTML se seznamem sociálních odkazů vyfiltrovaných podle tagu."""
    if style not in VALID_STYLES:
        style = "full"

    thumbnail_url = download_thumbnail(yt_id)

    template = _links_env.get_template("components/yt_iframe.html")
    return template.module.render_iframe(
        yt_id=yt_id,
        lang=lang,
        style=style,
        thumbnail_url=thumbnail_url,
    )
