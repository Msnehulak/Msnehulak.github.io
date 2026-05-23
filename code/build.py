import webbuilder as wb
import redirect as rd
import sweb

def generate_sitemap():
    # Základní URL adresa vašeho webu
    base_url = "https://msnehulak.github.io/"
    web_dir = sweb.BASE_DIR / "web"
    
    urls = []
    
    # Rekurzivně projde všechny soubory .html ve složce web
    for html_file in web_dir.rglob("*.html"):
        # Získá relativní cestu vůči složce web
        rel_path = html_file.relative_to(web_dir)
        # Převede cestu na posix formát s dopřednými lomítky
        url_path = rel_path.as_posix()
        
        # Hezké formátování URL adres (odstranění index.html na konci)
        if url_path == "index.html":
            full_url = base_url
        elif url_path.endswith("/index.html"):
            full_url = base_url + url_path[:-10]  # Odebere 'index.html'
        else:
            full_url = base_url + url_path
            
        urls.append(full_url)
    
    # Sestavení výsledného XML souboru
    xml_content = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml_content += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for url in sorted(urls):
        xml_content += f'  <url>\n    <loc>{url}</loc>\n  </url>\n'
    xml_content += '</urlset>'
    
    # Uložení sitemap.xml přímo do kořene složky web
    sitemap_path = web_dir / "sitemap.xml"
    with open(sitemap_path, "w", encoding="utf-8") as f:
        f.write(xml_content)
        
    print(f"Sitemap.xml úspěšně vygenerována s {len(urls)} odkazy.")

def page_404():
    text = sweb.data.texts["404"]
    bld = wb.WebBuilder(title=text["title"])
    bld.add_head(text["head"])

    abutf = wb.Frame()
    abutf.add_markdown(text["text"])
    abutf.move_main()
    bld.add_html(abutf.get_frame()) 

    bld.build()
    bld.save_web("404")

def projects_page():
    text = sweb.data.texts["projects"]
    bld = wb.WebBuilder(title=text["title"])
    bld.add_head(text["head"])

    abutf = wb.Frame()
    abutf.add_markdown(text["text"])
    abutf.move_main()
    bld.add_html(abutf.get_frame()) 

    bld.build()
    bld.save_web("projects")

def home_page():
    text = sweb.data.texts["home_page"]
    bld = wb.WebBuilder(title=text["title"])
    bld.add_head(text["head"])

    abutf = wb.Frame()
    abutf.add_markdown(text["text"])
    abutf.move_main()
    bld.add_html(abutf.get_frame()) 

    bld.build()
    bld.save_web("index")

def redirect():
    app = rd.Redirect()
    app.main()

def build():
    redirect()
    projects_page()
    home_page()
    page_404()
    generate_sitemap()

if __name__ == "__main__":
    build() 
