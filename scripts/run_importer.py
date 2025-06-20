import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from importer.import_to_db import push_csv_to_sqlite

if __name__ == "__main__":
    push_csv_to_sqlite(csv_path="data/raw/players.csv", db_path="data/mlb_history.db")
