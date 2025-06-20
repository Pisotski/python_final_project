import sqlite3
import csv
import os


def push_csv_to_sqlite(csv_path: str, db_path: str = "players.db"):
    if not os.path.exists(csv_path):
        print(f"[ERROR] File not found: {csv_path}")
        return

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS players (
                birth_name TEXT,
                nickname TEXT,
                born_on TEXT,
                born_in TEXT,
                died_on TEXT,
                died_in TEXT,
                cemetery TEXT,
                high_school TEXT,
                college TEXT,
                bats TEXT,
                throws TEXT,
                height TEXT,
                weight TEXT,
                first_game TEXT,
                last_game TEXT,
                draft TEXT,
                player_name TEXT
            )
        """
        )

        with open(csv_path, newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            rows = [
                (
                    row.get("Birth Name"),
                    row.get("Nickname"),
                    row.get("Born On"),
                    row.get("Born In"),
                    row.get("Died On"),
                    row.get("Died In"),
                    row.get("Cemetery"),
                    row.get("High School"),
                    row.get("College"),
                    row.get("Bats"),
                    row.get("Throws"),
                    row.get("Height"),
                    row.get("Weight"),
                    row.get("First Game"),
                    row.get("Last Game"),
                    row.get("Draft"),
                    row.get("Player Name"),
                )
                for row in reader
            ]

        if not rows:
            print(f"[WARNING] No rows found in CSV: {csv_path}")
            return

        cursor.executemany(
            """
            INSERT INTO players (
                birth_name, nickname, born_on, born_in, died_on, died_in,
                cemetery, high_school, college, bats, throws, height, weight,
                first_game, last_game, draft, player_name
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
            rows,
        )

        conn.commit()
        print(f"[SUCCESS] Inserted {len(rows)} rows into '{db_path}'.")

    finally:
        conn.close()
