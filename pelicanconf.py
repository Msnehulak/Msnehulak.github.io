AUTHOR = 'Snehulak'
SITENAME = 'Snehulak'
SITEURL = ''  # Pro lokální vývoj prázdné, publishconf.py si to pro produkci přepíše
PATH = 'content'
THEME = 'theme/0.1'
TIMEZONE = 'Europe/Rome'
DEFAULT_PAGINATION = False

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
    'de': 'Snehulak (DE)',
}

# --- 2. AUTOMATICKÉ NASTAVENÍ PRO PELICAN ---
DEFAULT_LANG = MAIN_LANG

# ZMĚNA: Pelican musí vidět VŠECHNY složky, aby dokázal spárovat překlady!
PAGE_PATHS = ['en'] 

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
            'I18N_TEMPLATES_LANG': 'en',
        }
