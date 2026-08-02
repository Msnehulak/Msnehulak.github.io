from datetime import datetime
import os
import sys
from pelican import signals
from jinja2 import Template
import subprocess

sys.path.append(os.curdir)

AUTHOR = 'Snehulak'
SITENAME = 'Snehulak'
SITEURL = os.environ.get('SITEURL', '')
PATH = 'content'
THEME = 'theme'
TIMEZONE = 'Europe/Rome'
DEFAULT_PAGINATION = False
STATIC_PATHS = ['images', 'favicon.ico']
TEMPLATE_PAGES = {
    'robots.txt': 'robots.txt'
}

year = datetime.now().year
start_year = 2026
if year == start_year: FOOTER_YEAR = f"2026"
else: FOOTER_YEAR = f"2026 - {year}"

# Vypneme generování zbytečných prázdných stránek pro blog
ARTICLE_PATHS = []
ARTICLE_SAVE_AS = ''
ARTICLE_LANG_SAVE_AS = ''
AUTHOR_SAVE_AS = ''
AUTHORS_SAVE_AS = ''
CATEGORY_SAVE_AS = ''
CATEGORIES_SAVE_AS = ''
TAG_SAVE_AS = ''
TAGS_SAVE_AS = ''
ARCHIVES_SAVE_AS = ''

FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

PLUGINS = [
    'pelican.plugins.i18n_subsites',
    'pelican.plugins.sitemap',
    'yaml_metadata',
]

SITEMAP = {
    'format': 'xml',
    'priorities': {
        'articles': 0.5,
        'indexes': 0.8,
        'pages': 0.7,
    },
    'changefreqs': {
        'articles': 'monthly',
        'indexes': 'daily',
        'pages': 'monthly',
    },
    'exclude': [
        'index/',
        'cs/index/',
        'index.html',
        'cs/index.html',
        'robots.txt',
        'cs/robots.txt'
    ]
}

RELATIVE_PATH = True

DELETE_OUTPUT_DIRECTORY = True

PAGE_URL = '{slug}/'
PAGE_SAVE_AS = '{slug}/index.html'

PAGE_LANG_URL = '{slug}/'
PAGE_LANG_SAVE_AS = '{slug}/index.html'

INDEX_SAVE_AS = 'index.html'
MAIN_LANG = 'en'

ALL_LANGUAGES = {
    'en': 'Snehulak (EN)',
    'cs': 'Snehulak (CS)',
}

DEFAULT_LANG = MAIN_LANG

PAGE_PATHS = ['', 'images'] 

JINJA_ENVIRONMENT = {
    'extensions': ['jinja2.ext.i18n']
}

I18N_TEMPLATES_LANG = None 

I18N_SUBSITES = {
    'cs': {
        'SITENAME': 'Snehulak (CS)',
    }
}

from build import get_web_data
from scripts.external_download import external_download
import xml.etree.ElementTree as ET

WEB_DATA = get_web_data()
def fill_data_to_md(content_objekt):
    """
    Tato funkce se spustí pokaždé, když Pelican otevře a načte jakýkoli .md soubor.
    Vezme jeho surový obsah a projede ho přes Jinja2 s daty z build.py.
    """
    if hasattr(content_objekt, '_content') and content_objekt._content:
        if getattr(content_objekt, '_already_rendered_by_jinja', False):
            return
        
        print(f">>> Upravuji Markdown pro soubor: {content_objekt.source_path}")
        
        surovy_text = content_objekt._content
        
        sablona = Template(surovy_text)
        upraveny_text = sablona.render(**WEB_DATA)
        
        content_objekt._content = upraveny_text

_ALREADY_STARTED = False

def first_start(pelican_obj):
    global _ALREADY_STARTED
    if _ALREADY_STARTED:
        return
    _ALREADY_STARTED = True

    external_download()

def clean_sitemap(pelican_obj):
    sitemap_path = os.path.join(pelican_obj.output_path, 'sitemap.xml')
    if not os.path.exists(sitemap_path):
        return

    # 1. Oprava atributu ref=" -> href="
    with open(sitemap_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    content = content.replace(' ref="', ' href="')

    # 2. Načtení XML
    ET.register_namespace('', 'http://www.sitemaps.org/schemas/sitemap/0.9')
    ET.register_namespace('xhtml', 'http://www.w3.org/1999/xhtml')
    
    tree = ET.ElementTree(ET.fromstring(content))
    root = tree.getroot()

    urls_map = {}

    # Projdeme všechny <url> elementy bez ohledu na namespace předponu
    for url_elem in list(root):
        loc_elem = None
        has_link = False

        for child in url_elem:
            # Najdeme prvek <loc>
            if child.tag.endswith('loc'):
                loc_elem = child
            # Zjistíme, zda blok obsahuje <xhtml:link> nebo jakýkoliv link
            elif child.tag.endswith('link'):
                has_link = True

        if loc_elem is not None and loc_elem.text:
            url_loc = loc_elem.text.strip()
            
            # Pokud danou URL ještě nemáme, NEBO pokud tato nová verze obsahuje xhtml:link,
            # uložíme si ji (upřednostníme blok s jazykovou mutací)
            if url_loc not in urls_map or has_link:
                urls_map[url_loc] = url_elem

    # Vyprázdníme staré elementy a vložíme pouze Unikátní/Sloučené
    root.clear()
    for clean_url_elem in urls_map.values():
        root.append(clean_url_elem)

    # Uložení opravené sitemap.xml
    tree.write(sitemap_path, encoding='utf-8', xml_declaration=True)
    print(">>> Sitemap byla úspěšně vyčištěna od duplicit a opravena!")


signals.finalized.connect(clean_sitemap)
signals.content_object_init.connect(fill_data_to_md)
signals.initialized.connect(first_start)


