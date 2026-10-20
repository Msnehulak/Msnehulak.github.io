from src import pages_db, pages_worker

pages_db.init_sqlite_DB()

app = pages_worker.IndexContent()
