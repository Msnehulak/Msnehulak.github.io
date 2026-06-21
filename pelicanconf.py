# pelicanconf.py

TIMEZONE = 'Europe/Prague'
DEFAULT_LANG = 'en'

# Ignorovat výchozí rozvržení pro blogy
DIRECT_TEMPLATES = []
# Sledovat složky pro stránky a redirecty
PAGE_PATHS = ['pages', 'r']

# Řekni Pelicanu, aby sledoval složku theme i images uvnitř složky content
STATIC_PATHS = ['theme', 'images']

# Přesměrování style.css přímo do kořene outputu
EXTRA_PATH_METADATA = {
    'theme/style.css': {'path': 'style.css'},
}

THEME = 'theme'
_404_SAVE_AS = '404.html'
