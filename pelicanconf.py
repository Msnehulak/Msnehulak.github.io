AUTHOR = 'Snehulak'
SITENAME = 'Snehulak'
SITEURL = ""
PATH = "content"
THEME = "theme/0.1"
TIMEZONE = 'Europe/Rome'
DEFAULT_LANG = 'en'
DEFAULT_PAGINATION = False

# 1. Všechno v 'content' budeme brát jako statické stránky (Pages)
PAGE_PATHS = ['']
PAGE_URL = '{slug}/'
PAGE_SAVE_AS = '{slug}/index.html'
INDEX_SAVE_AS = 'index.html'

# Pokud máte podsložky (např. content/o-nas/index.md -> o-nas/index.html), použijte toto:
# PAGE_URL = '{path_no_ext}.html'
# PAGE_SAVE_AS = '{path_no_ext}.html'

# 2. Vypnutí článků (Articles) a všech jejich automatických výstupů
ARTICLE_PATHS = []
ARTICLE_SAVE_AS = ''
ARTICLE_LANG_SAVE_AS = ''

# 3. Ignorovat CSS a JS, aby se negenerovaly jako samostatné stránky
ARTICLE_EXCLUDES = ['css', 'js', 'r']
PAGE_EXCLUDES = ['css', 'js', 'r']

# 4. Statické soubory, které se mají pouze zkopírovat (CSS, JS, soubory v 'r')
STATIC_PATHS = ['css', 'js', 'r']

# Ostatní vypínací direktivy (ponechat prázdné)
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

DELETE_OUTPUT_DIRECTORY = True

