import argparse
import os
import shutil
from pathlib import Path

from src import (
    cache_manager,
    index_content,
    mearge_page,
    pages_bulder,
    pages_db,
    run_node,
)

parser = argparse.ArgumentParser()
parser.add_argument("--no-cache", action="store_true")
args = parser.parse_args()
if args.no_cache:
    cache_manager.get_cache().clear()

pages_db.init_sqlite_DB()

index_content.IndexContent()

mearge_page.link_language_versions()

pages_bulder.PagesBuilder().main()

# Tailwind až nakonec, nad hotovým output/
run_node.run_tailwind()

src = Path("theme/static")
dst = Path("output/static")
if os.path.exists(dst):
    shutil.rmtree(dst)

shutil.copytree(src, dst)
