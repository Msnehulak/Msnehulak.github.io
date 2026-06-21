# code/build.py
import sweb
import osu
import redirect as rd
import shutil
from pathlib import Path

def create_markdown_page(lang, page_key, prefix):
    """Vezme texty z text.json a uloží je jako Markdown pro Pelican."""
    text_data = sweb.data.texts[lang][page_key]
    
    # Detekce názvu souboru (index, projects, 404)
    filename = "index" if page_key == "home_page" else page_key
    
    # Vyčištění textu od tvé staré značky ,nl.
    clean_text = text_data["text"].replace(",nl.", "\n")
    
    # Metadata pro Pelican (Front Matter)
    md_content = f"""Title: {text_data["title"]}
Lang: {lang}
Slug: {filename}
Save_as: {prefix}{filename}.html
URL: {prefix}{filename}.html

{clean_text}
"""
    
    # Určení cílové cesty v content/pages/
    target_dir = sweb.BASE_DIR / "content" / "pages" / prefix
    target_dir.mkdir(parents=True, exist_ok=True)
    
    with open(target_dir / f"{filename}.md", "w", encoding="utf-8") as f:
        f.write(md_content)

def prepare_theme():
    """Zkopíruje stávající style.css do složky, kterou Pelican uvidí."""
    src_css = sweb.BASE_DIR / "data" / "style.css"
    dst_dir = sweb.BASE_DIR / "content" / "theme"
    dst_dir.mkdir(parents=True, exist_ok=True)
    if src_css.exists():
        shutil.copy2(src_css, dst_dir / "style.css")

def build():
    prepare_theme()
    
    # 1. Zpracování redirectů přes tvůj upravený redirect.py
    app_rd = rd.Redirect()
    app_rd.main()
    
    # 2. Aktualizace dat pro osu
    osu.osu.update_data()
    
    # 3. Generování stránek (anglické do kořene, české do cz/)
    for lang, prefix in [("en", ""), ("cs", "cz/")]:
        create_markdown_page(lang, "home_page", prefix)
        create_markdown_page(lang, "projects", prefix)
        create_markdown_page(lang, "404", prefix)
        
        # Osu má specifickou logiku, vygenerujeme ji zvlášť
        osu.osu.create_page(lang, prefix)
     
if __name__ == "__main__":
    build()
