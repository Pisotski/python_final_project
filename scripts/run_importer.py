import logging
import sqlite3

import pandas as pd
from constants.paths import DB_PATH
from data.data_cleaner.data_cleaner import load_and_clean
from importer.importer_utils import enrich_review_with_player_id
from importer.push_df_to_sqlite import push_df_to_sqlite, push_players_to_sqlite

logging.basicConfig(level=logging.INFO)


def main():

    try:
        players_biography_df = load_and_clean("data/raw/players.csv")
        push_players_to_sqlite(
            players_biography_df,
            db_path=DB_PATH,
            table_name="players",
        )
        with sqlite3.connect(DB_PATH) as conn:

            df_player_review = pd.read_csv("data/raw/player_review.csv")
            df_player_review = enrich_review_with_player_id(df_player_review, conn)
            push_df_to_sqlite(
                df_player_review,
                db_path=DB_PATH,
                table_name="player_review",
            )

            df_pitcher_review = pd.read_csv("data/raw/pitcher_review.csv")
            df_pitcher_review = enrich_review_with_player_id(df_pitcher_review, conn)
            push_df_to_sqlite(
                df_pitcher_review,
                db_path=DB_PATH,
                table_name="pitcher_review",
            )
    except Exception as e:
        logging.exception("Failed to import player data")


if __name__ == "__main__":
    main()
