import logging
import os
import xml.etree.ElementTree as ET
from pathlib import Path

from scripts import sweb

SVG_NS = "http://www.w3.org/2000/svg"
ET.register_namespace("", SVG_NS)

BUILD_IMG_PATH = sweb.BASE_DIR / "content" / "images" / "build"
OUTPUT_PATH = sweb.BASE_DIR / "output"
RASTER_IMGES_TYPES = (".png", ".jpeg", ".webp", ".jpg")
SVG_OUTPUT_NAME = "sprite.svg"


class Images:
    def __init__(self) -> None:
        pass

    def optimize_output(self):
        img_folders = self._get_img_paths()
        for folder in img_folders:
            self.optimize_folder(folder)

    @staticmethod
    def _get_img_paths():
        img_folders = []
        content_dir = OUTPUT_PATH
        for img_dir in content_dir.rglob("images"):
            if img_dir.is_dir():
                img_folders.append(img_dir)
        return img_folders

    def optimize_folder(self, folder):
        self.folder = folder
        files = os.listdir(self.folder)

        self.svg_list = []
        self.raster_list = []

        for file in files:
            if file.endswith(RASTER_IMGES_TYPES):
                self.raster_list.append(file)
            elif file.endswith(".svg"):
                self.svg_list.append(file)

        if len(self.svg_list) > 0:
            self.optimize_svg()

        if len(self.raster_list) > 0:
            self.optimize_raster()

    def optimize_svg(self):
        input_folder = self.folder

        output_file = input_folder / f"{Path(SVG_OUTPUT_NAME).stem}.svg"

        root_svg = ET.Element(f"{{{SVG_NS}}}svg")

        for filename in sorted(os.listdir(input_folder)):
            if filename.endswith(".svg"):
                file_path = os.path.join(input_folder, filename)
                symbol_id = os.path.splitext(filename)[0]
                try:
                    tree = ET.parse(file_path)
                    src_svg = tree.getroot()
                    symbol = ET.Element(f"{{{SVG_NS}}}symbol", {"id": symbol_id})
                    viewbox = src_svg.get("viewBox")
                    if viewbox:
                        symbol.set("viewBox", viewbox)
                    for child in src_svg:
                        fix_namespace(child)
                        symbol.append(child)
                    root_svg.append(symbol)
                except ET.ParseError as e:
                    logging.error(f"While working on {filename}: {e}")

        sprite_tree = ET.ElementTree(root_svg)
        self.clear_from_svg()
        sprite_tree.write(output_file, encoding="utf-8", xml_declaration=True)
        logging.info(f">>> Sprite created: {output_file}")

    def clear_from_svg(self):
        for svg in self.svg_list:
            rm_file = self.folder / svg
            Path.unlink(rm_file)

    def optimize_raster(self):
        pass


def fix_namespace(element):
    if not element.tag.startswith("{"):
        element.tag = f"{{{SVG_NS}}}{element.tag}"

    if "xmlns" in element.attrib:
        del element.attrib["xmlns"]

    for child in element:
        fix_namespace(child)


if __name__ == "__main__":
    app = Images()
    app.optimize_output()
