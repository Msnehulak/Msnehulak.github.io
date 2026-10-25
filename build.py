import os
import shutil
from pathlib import Path

from src import index_content, mearge_page, pages_bulder, pages_db, run_node

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
