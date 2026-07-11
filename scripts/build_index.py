from pathlib import Path
import xml.etree.ElementTree as ET
import yaml

BASE_DIR = Path(__file__).resolve().parent.parent
LINKS = BASE_DIR / 'data' / 'links.yaml'
IMG_CLASS_NAME = 'index-img'
LINKS_CLASS = 'links-index' 
IMG_PATH_START = 'icon/btrace' # /trace

def get_links_html(lan='en'):
    with open(LINKS, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)

    if not data:
        return ''

    html_elements = [f'<div class="{LINKS_CLASS}">']

    for link in data:
        url = link['link']
        
        # 1. Vytvoříme element <button> s JavaScriptem pro otevření odkazu
        button_element = ET.Element('button', {
            'type': 'button',
            'onclick': f"window.open('{url}', '_blank')",
            'class': 'index-btn'  # Můžeš mu dát vlastní třídu pro stylování v CSS
        })

        # 2. Vytvoříme vnořený obrázek <img>
        img_path = f"/images/{IMG_PATH_START}/{link['img']}"
        alt_text = link['hover'][lan]
        
        ET.SubElement(button_element, 'img', {
            'src': img_path,
            'alt': alt_text,
            'title': alt_text,
            'class': IMG_CLASS_NAME
        })

        # 3. Převedeme element na HTML text
        html_string = ET.tostring(button_element, encoding='unicode')
        html_elements.append(html_string)
    html_elements.append('</div>')    
    return ''.join(html_elements)

if __name__ == '__main__':
    print("CS verze s tlačítky:")
    print(get_links_html('cs'))
