if __name__ == '__main__': import sweb
else: from . import sweb
import os
import xml.etree.ElementTree as ET

SVG_NS = "http://www.w3.org/2000/svg"
ET.register_namespace("", SVG_NS)

BUILD_IMG_PATH = sweb.BASE_DIR / 'content' / 'images' / 'build'

class SvgEditor:
    def __init__(self) -> None:
        pass

def fix_namespace(element):
    if not element.tag.startswith('{'):
        element.tag = f"{{{SVG_NS}}}{element.tag}"
    
    if "xmlns" in element.attrib:
        del element.attrib["xmlns"]
        
    for child in element:
        fix_namespace(child)

def create_svg_sprite(input_folder, output_file):
    root_svg = ET.Element(f"{{{SVG_NS}}}svg")

    for filename in sorted(os.listdir(input_folder)):
        if filename.endswith(".svg"):
            file_path = os.path.join(input_folder, filename)
            symbol_id = os.path.splitext(filename)[0]

            try:
                tree = ET.parse(file_path)
                src_svg = tree.getroot()

                symbol = ET.Element(f"{{{SVG_NS}}}symbol", {"id": symbol_id})

                # Kopírování viewBox
                viewbox = src_svg.get("viewBox")
                if viewbox:
                    symbol.set("viewBox", viewbox)

                for child in src_svg:
                    fix_namespace(child)
                    symbol.append(child)

                root_svg.append(symbol)

            except ET.ParseError as e:
                print(f"Chyba při zpracování {filename}: {e}")

    sprite_tree = ET.ElementTree(root_svg)
    sprite_tree.write(
        output_file, encoding="utf-8", xml_declaration=True
    )
    print(f">>> Sprite úspěšně vytvořen: {output_file}")

def image_main():
    imgs_path = sweb.BASE_DIR / 'content' / 'images' / 'icon'
    img_path = BUILD_IMG_PATH / 'icon.svg'
    create_svg_sprite(imgs_path, img_path)

if __name__ == '__main__':
    image_main()
