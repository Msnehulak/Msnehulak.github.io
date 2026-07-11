import os
import sys
from pelican import signals
from jinja2 import Template

# Aby Python viděl build.py v aktuálním adresáři
sys.path.append(os.curdir)

# Importujeme tvou funkci z build.py
from build import get_web_data

# Načteme data z API hned při startu Pelicanu (aby se nevolalo pro každý soubor znovu)
WEB_DATA = get_web_data()

def fill_data_to_md(content_objekt):
    """
    Tato funkce se spustí pokaždé, když Pelican otevře a načte jakýkoli .md soubor.
    Vezme jeho surový obsah a projede ho přes Jinja2 s daty z build.py.
    """
    if hasattr(content_objekt, '_content') and content_objekt._content:
        print(f">>> Upravuji Markdown pro soubor: {content_objekt.source_path}")
        
        surovy_text = content_objekt._content
        
        sablona = Template(surovy_text)
        upraveny_text = sablona.render(**WEB_DATA)
        
        content_objekt._content = upraveny_text

signals.content_object_init.connect(fill_data_to_md)

AUTHOR = 'Snehulak'
SITENAME = 'Snehulak'
SITEURL = ''  # Pro lokální vývoj prázdné, publishconf.py si to pro produkci přepíše
PATH = 'content'
THEME = 'theme'
TIMEZONE = 'Europe/Rome'
DEFAULT_PAGINATION = False
STATIC_PATHS = ['images']

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

RELATIVE_PATH = True

DELETE_OUTPUT_DIRECTORY = True

# Nastavení URL adres pro čisté složky
PAGE_URL = '{slug}/'
PAGE_SAVE_AS = '{slug}/index.html'

# Přidej tyto dva řádky pro správné párování překladů:
PAGE_LANG_URL = '{slug}/'
PAGE_LANG_SAVE_AS = '{slug}/index.html'

INDEX_SAVE_AS = 'index.html'

# --- 1. JAZYKOVÁ KONFIGURACE (ZDE DIKTUJEŠ HLAVNÍ JAZYK) ---
MAIN_LANG = 'en'  # Stačí změnit na 'cz', 'de' atd. a celý web se přenastaví sám

# Seznam všech podporovaných jazyků na webu
ALL_LANGUAGES = {
    'en': 'Snehulak (EN)',
    'cs': 'Snehulak (CS)',
}

# --- 2. AUTOMATICKÉ NASTAVENÍ PRO PELICAN ---
DEFAULT_LANG = MAIN_LANG

# ZMĚNA: Pelican musí vidět VŠECHNY složky, aby dokázal spárovat překlady!
PAGE_PATHS = ['en', 'cs', 'images'] 

PLUGINS = ['pelican.plugins.i18n_subsites']
JINJA_ENVIRONMENT = {
    'extensions': ['jinja2.ext.i18n']
}
I18N_TEMPLATES_LANG = 'en'

# --- 3. DYNAMICKÉ GENEROVÁNÍ SUBWEBŮ ---
I18N_SUBSITES = {}
for lang_code, site_name in ALL_LANGUAGES.items():
    if lang_code != MAIN_LANG:
        I18N_SUBSITES[lang_code] = {
            'PAGE_PATHS': [lang_code],
            'SITENAME': site_name,
            'I18N_TEMPLATES_LANG': None,
        }
