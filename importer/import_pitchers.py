import logging
import pandas as pd
from importer.push_df_to_sqlite import push_df_to_sqlite

logging.basicConfig(level=logging.INFO)


def main():
    try:
        df = pd.read_csv("data/raw/pitchers.csv")
        push_df_to_sqlite(df, "data/mlb_players.db", "pitchers")
    except Exception as e:
        logging.exception("Failed to import pitchers")


if __name__ == "__main__":
    main()
