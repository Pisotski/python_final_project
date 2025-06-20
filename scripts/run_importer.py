import logging
from data.data_cleaner.data_cleaner import load_and_clean
from importer.import_to_db import push_df_to_sqlite

logging.basicConfig(level=logging.INFO)


def main():
    try:
        df = load_and_clean("data/raw/players.csv")
        push_df_to_sqlite(
            df,
            db_path="data/mlb_players.db",
            table_name="players",
        )
    except Exception as e:
        logging.exception("Failed to import player data")


if __name__ == "__main__":
    main()
