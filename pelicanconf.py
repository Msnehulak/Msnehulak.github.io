import logging
import os
import sys

sys.path.append(os.curdir)

import subprocess
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
from jinja2 import Template
from pelican import signals

from scripts import sweb

load_dotenv()

sys.path.append(os.curdir)

AUTHOR = "Snehulak"
SITENAME = "Snehulak"
SITEURL_ORG = os.getenv("SITEURL", "https://example.com").rstrip("/")
SITEURL = SITEURL_ORG
RELATIVE_URLS = True
PATH = "content"
THEME = "theme"
TIMEZONE = "Europe/Rome"
DEFAULT_PAGINATION = False
STATIC_PATHS = ["favicon.ico"]
TEMPLATE_PAGES = {"robots.txt": "robots.txt", "sitemap.xml": "sitemap.xml"}

year = datetime.now().year
start_year = 2026
if year == start_year:
    FOOTER_YEAR = f"2026"
else:
    FOOTER_YEAR = f"2026 - {year}"

ARTICLE_PATHS = []
ARTICLE_SAVE_AS = ""
ARTICLE_LANG_SAVE_AS = ""
AUTHOR_SAVE_AS = ""
AUTHORS_SAVE_AS = ""
CATEGORY_SAVE_AS = ""
CATEGORIES_SAVE_AS = ""
TAG_SAVE_AS = ""
TAGS_SAVE_AS = ""
ARCHIVES_SAVE_AS = ""

FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

PLUGINS = [
    "pelican.plugins.i18n_subsites",
    "yaml_metadata",
    "pelican_katex",
]

RELATIVE_PATH = False

DELETE_OUTPUT_DIRECTORY = True

PAGE_URL = "{slug}/"
PAGE_SAVE_AS = "{slug}/index.html"

PAGE_LANG_URL = "{lang}/{slug}/"
PAGE_LANG_SAVE_AS = "{lang}/{slug}/index.html"

content_dir = Path(PATH)
for img_dir in content_dir.rglob("images"):
    if img_dir.is_dir():
        STATIC_PATHS.append(str(img_dir.relative_to(content_dir)))

INDEX_SAVE_AS = "index.html"
MAIN_LANG = "en"

ALL_LANGUAGES = {
    "en": "Snehulak (EN)",
    "cs": "Snehulak (CS)",
}

DEFAULT_LANG = MAIN_LANG

PAGE_PATHS = [""]

JINJA_ENVIRONMENT = {
    #    'extensions': ['jinja2.ext.i18n']
}

JINJA_GLOBALS = {
    "now": datetime.now(),
    "NAV": {
        "cs": {key: val["cs"] for key, val in sweb.data["tran"]["nav"].items()},
        "en": {key: val["en"] for key, val in sweb.data["tran"]["nav"].items()},
    },
}

I18N_TEMPLATES_LANG = None

i18n_all_subsites = {
    "en": {
        "SITENAME": "Snehulak (EN)",
        "SITEURL": f"{SITEURL}/en",
    },
    "cs": {
        "SITENAME": "Snehulak (CS)",
        "SITEURL": f"{SITEURL}/cs",
    },
}

I18N_SUBSITES = {}
for lan, val in i18n_all_subsites.items():
    if not lan == MAIN_LANG:
        I18N_SUBSITES[lan] = val

from scripts import create_redirects, external_download, image, sweb, update_page

_ALREADY_STARTED = False


def first_start(pelican_obj):
    global _ALREADY_STARTED
    if _ALREADY_STARTED:
        return
    if os.environ.get("PELICAN_RUNNING_RELOAD") == "true":
        pass
    _ALREADY_STARTED = True

    sweb.create_paths()
    external_download.external_download()


def on_finalized(pelican_obj):
    app_image = image.Images()
    app_image.optimize_output()
    create_redirects.main()
    external_download.move_file()


def on_initialized(pelican_obj):
    if not _ALREADY_STARTED:
        first_start(pelican_obj)


signals.finalized.connect(on_finalized)
signals.initialized.connect(on_initialized)
signals.content_object_init.connect(update_page.update_page)
