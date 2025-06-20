## FIXME:
from utils.db_utils import push_csv_to_sqlite

if __name__ == "__main__":
    push_csv_to_sqlite(csv_path="data/scraped_data.csv", db_path="db/players.db")