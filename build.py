import os
import shutil
from pathlib import Path

from src import pages_bulder, pages_db, pages_worker, run_node

pages_db.init_sqlite_DB()

app = pages_worker.IndexContent()
pages_bulder.PagesBuilder().main()

# Tailwind až nakonec, nad hotovým output/
run_node.run_tailwind()

src = Path("theme/static")
dst = Path("output/static")
if os.path.exists(dst):
    shutil.rmtree(dst)

shutil.copytree(src, dst)
