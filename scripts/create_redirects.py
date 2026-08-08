if __name__ == '__main__': import sweb
else: from . import sweb
import xml.etree.ElementTree as ET
import os
from pathlib import Path

PATH = sweb.BASE_DIR / 'output' / 'sitemap.xml'
OUTPUT_PATH = sweb.BASE_DIR / 'redirect' 

def main():
    if not PATH.exists():
        print(f">>> Soubor {PATH} zatím neexistuje, přeskakuji přesměrování.")
        return
    tree = ET.parse(PATH)
    root = tree.getroot()

    urls = set()
    for elem in root.iter():
        if elem.tag.endswith("loc") and elem.text:
            urls.add(elem.text.strip())
        elif elem.tag.endswith("link") and elem.attrib.get("href"):
            urls.add(elem.attrib["href"].strip())

    for url in urls:
        path = url.split("://")[-1].split("/", 1)[-1]
        
        # Odstraníme koncový lomítko pro správný název složky
        dir_path = path.strip("/")
        dir_path = OUTPUT_PATH / dir_path
        
        os.makedirs(dir_path, exist_ok=True)
        
        html_content = f"""<!DOCTYPE html>
    <html>
    <head>
        <meta http-equiv="refresh" content="0; url={url}">
        <script>window.location.href = "{url}";</script>
    </head>
    <body>
        <p>Pokud nebudete přesměrováni, klikněte <a href="{url}">zde</a>.</p>
    </body>
    </html>"""
        
        with open(os.path.join(dir_path, "index.html"), "w", encoding="utf-8") as f:
            f.write(html_content)

    print("Složky a přesměrování byly úspěšně vytvořeny!")

if __name__ == '__main__':
    main()
