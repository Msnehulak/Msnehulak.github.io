import webbuilder as wb
import redirect as rd
import osu
import sweb
import shutil

def generate_sitemap():
    base_url = "https://msnehulak.github.io/"
    web_dir = sweb.BASE_DIR / "web"
    
    urls = []
    
    for html_file in web_dir.rglob("*.html"):
        rel_path = html_file.relative_to(web_dir)
        url_path = rel_path.as_posix()
        
        if url_path == "index.html":
            full_url = base_url
        elif url_path.endswith("/index.html"):
            full_url = base_url + url_path[:-10]
        else:
            full_url = base_url + url_path
            
        urls.append(full_url)
    
    xml_content = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml_content += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for url in sorted(urls):
        xml_content += f'  <url>\n    <loc>{url}</loc>\n  </url>\n'
    xml_content += '</urlset>'
  
    sitemap_path = web_dir / "sitemap.xml"
    with open(sitemap_path, "w", encoding="utf-8") as f:
        f.write(xml_content)
        
    print(f"Sitemap.xml úspěšně vygenerována s {len(urls)} odkazy.")

def page_404(lang, prefix):
    text = sweb.data.texts[lang]["404"]
    css = "../style.css" if lang == "cs" else "style.css"
    # ZMĚNA: Přidán parametr current_page="404"
    bld = wb.WebBuilder(title=text["title"], lang=lang, css_path=css, current_page="404")
    bld.add_head(text["head"])

    abutf = wb.Frame()
    abutf.add_markdown(text["text"])
    abutf.move_main()
    bld.add_html(abutf.get_frame()) 

    bld.build()
    bld.save_web(f"{prefix}404")

def projects_page(lang, prefix):
    text = sweb.data.texts[lang]["projects"]
    css = "../style.css" if lang == "cs" else "style.css"
    # ZMĚNA: Přidán parametr current_page="projects"
    bld = wb.WebBuilder(title=text["title"], lang=lang, css_path=css, current_page="projects")
    bld.add_head(text["head"])

    abutf = wb.Frame()
    abutf.add_markdown(text["text"])
    abutf.move_main()
    bld.add_html(abutf.get_frame()) 

    bld.build()
    bld.save_web(f"{prefix}projects")

def home_page(lang, prefix):
    text = sweb.data.texts[lang]["home_page"]
    css = "../style.css" if lang == "cs" else "style.css"
    # ZMĚNA: Přidán parametr current_page="index"
    bld = wb.WebBuilder(title=text["title"], lang=lang, css_path=css, current_page="index")
    bld.add_head(text["head"])

    abutf = wb.Frame()
    abutf.add_markdown(text["text"])
    abutf.move_main()
    bld.add_html(abutf.get_frame()) 

    bld.build()
    bld.save_web(f"{prefix}index")

def redirect():
    app = rd.Redirect()
    app.main()

def prepare_folders():
    web_dir = sweb.BASE_DIR / "web"
    data_dir = sweb.BASE_DIR / "data"
    
    web_dir.mkdir(parents=True, exist_ok=True)
    
    src_css = data_dir / "style.css"
    dst_css = web_dir / "style.css"
    
    if src_css.exists():
        shutil.copy2(src_css, dst_css)
        print("Soubor style.css byl úspěšně zkopírován do složky web.")
    else:
        print("Upozornění: Soubor data/style.css nebyl nalezen!")

def build():
    prepare_folders()
    redirect()
    
    # Aktualizace dat pro osu proběhne před stavbou stránek
    osu.osu.update_data()
    
    # Generování webu pro angličtinu (kořen) a češtinu (složka cz/)
    for lang, prefix in [("en", ""), ("cs", "cz/")]:
        projects_page(lang, prefix)
        home_page(lang, prefix)
        page_404(lang, prefix)
        osu.osu.create_page(lang, prefix)
        
    generate_sitemap()
     
if __name__ == "__main__":
    build()
