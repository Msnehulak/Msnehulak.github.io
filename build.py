from src import pages_bulder, pages_db, pages_worker, run_node

pages_db.init_sqlite_DB()

app = pages_worker.IndexContent()
pages_bulder.PagesBuilder().main()

# Tailwind až nakonec, nad hotovým output/
run_node.run_tailwind()
