from datetime import datetime
import os
import sys
from pelican import signals
from jinja2 import Template
import subprocess
import re
import xml.etree.ElementTree as ET
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

sys.path.append(os.curdir)

AUTHOR = 'Snehulak'
SITENAME = 'Snehulak'
SITEURL = os.getenv('SITEURL', 'https://example.com').rstrip('/')
PATH = 'content'
THEME = 'theme'
TIMEZONE = 'Europe/Rome'
DEFAULT_PAGINATION = False
STATIC_PATHS = ['images', 'favicon.ico']
TEMPLATE_PAGES = {
    'robots.txt': 'robots.txt',
    'sitemap.xml': 'sitemap.xml'
}

year = datetime.now().year
start_year = 2026
if year == start_year: FOOTER_YEAR = f"2026"
else: FOOTER_YEAR = f"2026 - {year}"

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
    'yaml_metadata',
    'pelican_katex',
]

RELATIVE_PATH = False 

DELETE_OUTPUT_DIRECTORY = True

PAGE_URL = '{slug}/'
PAGE_SAVE_AS = '{slug}/index.html'

PAGE_LANG_URL = '{lang}/{slug}/'
PAGE_LANG_SAVE_AS = '{lang}/{slug}/index.html'

content_dir = Path(PATH)
for img_dir in content_dir.rglob('images'):
    if img_dir.is_dir():
        STATIC_PATHS.append(str(img_dir.relative_to(content_dir)))

INDEX_SAVE_AS = 'index.html'
MAIN_LANG = 'en'

ALL_LANGUAGES = {
    'en': 'Snehulak (EN)',
    'cs': 'Snehulak (CS)',
}

DEFAULT_LANG = MAIN_LANG

PAGE_PATHS = ['', 'images']

JINJA_ENVIRONMENT = {
#    'extensions': ['jinja2.ext.i18n']
}

JINJA_GLOBALS = {
    'now': datetime.now()
}

I18N_TEMPLATES_LANG = None 

i18n_all_subsites = {
    'en': {
        'SITENAME': 'Snehulak (EN)',
        'SITEURL': f'{SITEURL}/en',
    },
    'cs': {
        'SITENAME': 'Snehulak (CS)',
        'SITEURL': f'{SITEURL}/cs',
    }
}

I18N_SUBSITES = {}
for lan, val in i18n_all_subsites.items():
    if not lan == MAIN_LANG:
        I18N_SUBSITES[lan] = val

from build import get_web_data
from scripts import sweb, image, external_download

WEB_DATA = get_web_data()
def fill_data_to_md(content_objekt):
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
    if os.environ.get('PELICAN_RUNNING_RELOAD') == 'true':
        pass
    _ALREADY_STARTED = True

    sweb.create_paths()
    external_download.external_download()

def set_custom_page_urls(content_obj):
    if not hasattr(content_obj, 'slug'):
        return

    if hasattr(content_obj, 'metadata') and content_obj.metadata:
        # 1. Hlavní strana (index)
        if content_obj.slug == 'index':
            content_obj.override_url = ''
            content_obj.override_save_as = 'index.html'
            return

        # 2. Vlastní složka pro ostatní stránky (např. folder: projects)
        folder = content_obj.metadata.get('folder')
        if folder:
            folder = folder.strip('/')
            content_obj.override_url = f"{folder}/{content_obj.slug}/"
            content_obj.override_save_as = f"{folder}/{content_obj.slug}/index.html"
        else:
            content_obj.override_url = f"{content_obj.slug}/"
            content_obj.override_save_as = f"{content_obj.slug}/index.html"

def on_finalized(pelican_obj):
    app_image = image.Images()
    app_image.optimize_output()

def on_initialized(pelican_obj):
    if not _ALREADY_STARTED:
        first_start(pelican_obj)

signals.finalized.connect(on_finalized)
signals.initialized.connect(on_initialized)
signals.content_object_init.connect(set_custom_page_urls)
signals.content_object_init.connect(fill_data_to_md)

